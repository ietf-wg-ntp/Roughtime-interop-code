import sys
import os
import yaml
import logging
import datetime
import argparse
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
    parser.add_argument('--runner', default='docker',
                        help='Path to a different container runtime')
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
        logger.critical('Implementations YAML appaers bad, exiting...')
        sys.exit(1)

    # Generate all the permutations of client and servers
    permutations = generate_permutations(args.impls['implementations'])

    # Prepare the location
    start_time = datetime.datetime.now(datetime.UTC)
    # Colons and other characters can be iffy in folder names
    results_dir = start_time.strftime("%Y%m%dT%H%M%SZ")

    if args.dry_run:
        logger.info('Dry-run: Create folder {results_dir}')
    else:
        # os.mkdir()

        pass

    # For each generate the docker command to run for them
    for perm in permutations:
        cmd = generate_cmd(perm)


# Generate the docker command to run for a given permutation
def generate_cmd(perm: Dict) -> str:
    return ""


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
