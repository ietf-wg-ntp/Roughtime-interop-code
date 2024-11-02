import sys
import os
import yaml
import logging
import datetime
import argparse
import subprocess
from argparse import ArgumentParser
from typing import Dict, List

CMD_INFO = """
plummet takes all the known roughtime implementations and attempts to perform
interop tests against each client/server pair.
"""


def main() -> None:
    parser = ArgumentParser(description=CMD_INFO)
    parser.add_argument('--impls', type=argparse.FileType('r'),
                        default='implementations/implementations.yml',
                        help='Path to the implementations YAML file')
    parser.add_argument('--output-dir', default='results/',
                        help='Base directory to write data out to')
    parser.add_argument('--dry-run', action=argparse.BooleanOptionalAction,
                        help="Don't make any system calls, just print")
    parser.add_argument('--container', type=str, default='/usr/local/bin/docker',
                        help='Path to docker or your preferred container manager')
    parser.add_argument('--perm-config', type=str, default='etc/permutation.yml',
                        help='Path to the ')
    parser.add_argument('--timeout', default=10,
                        help='Timeout in seconds for each permutation run')
    parser.add_argument('--verbose', action=argparse.BooleanOptionalAction,
                        help='Enable more verbosity')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('plummet')

    try:
        args.impls = yaml.safe_load(args.impls.read())
    except yaml.YAMLError as e:
        logger.critical('Implementations YAML appears bad, exiting...')
        sys.exit(1)

    # Generate all the permutations of client and servers
    permutations = generate_permutations(args.impls['implementations'])

    # Prepare the location
    start_time = datetime.datetime.now(datetime.timezone.utc)
    results_dir = start_time.strftime("%Y%m%dT%H%M%SZ") # Colons can be iffy
    if not os.path.isabs(args.output_dir):
        output_dir = os.path.join(os.path.abspath(args.output_dir), results_dir)
    else:
        output_dir = os.path.join(args.output_dir, results_dir)
    logger.debug(f'Results directory: {output_dir}')

    if not args.dry_run:
        os.mkdir(output_dir)
    
    logger.debug(f'Iterating over {len(permutations)} permutations')

    # Iterate through each permutation, create a subdirectory, and run
    for perm in permutations:
        perm_dir = os.path.join(output_dir, '_'.join([perm['server'], perm['client']]))
        logger.debug(f'Preparing to run for server: {perm["server"]} client: {perm["client"]}')
        # These environment variables **must** match whatever we use in the
        # permutations container configuration file, or else computer will be
        # very sad with us, and nobody wants that.
        env = {
            'SERVER_IMAGE': f'plummet-{perm["server"]}:latest',
            'CLIENT_IMAGE': f'plummet-{perm["client"]}:latest',
            'PERM_DIR': perm_dir
        }

        logger.debug(f'Creating permutation directory {perm_dir}')
        if not args.dry_run:
            os.mkdir(perm_dir)

        # This could blow up if you have spaces in the full path, watch out!
        perm_config = os.path.abspath(args.perm_config)
        perm_cmd = f'{args.container} compose -f {perm_config} up'
        logger.debug(f'Running `{perm_cmd}` with a {args.timeout} second timeout...')
        logger.debug

        if args.dry_run:
            logging.info('This is the bit where we pretend to run, but are not!')
            continue

        # Let's run (away from all our problems)
        perm_process = subprocess.Popen(perm_cmd.split(' '), env=env)
        try:
            perm_process.wait(args.timeout)
        except subprocess.TimeoutExpired:
            perm_process.kill()
            logger.warn(f'Terminating server: {perm["server"]} client: {perm["client"]}')
        cleanup_cmd = f'{args.container} compose -f {perm_config} down --remove-orphans'
        subprocess.run(cleanup_cmd.split(' '), env=env)

# For each implementation that we know of, based on it having a client and/or
# server, work out permutations of all.
def generate_permutations(impls: List[Dict]) -> List[Dict]:
    permutations = []
    for server in impls:
        if not impls[server]['enabled'] or not impls[server]['server']:
            continue
        for client in impls:
            if not impls[client]['enabled'] or not impls[client]['client']:
                continue
            permutations.append({
                'server': server,
                'client': client
            })
    return permutations
