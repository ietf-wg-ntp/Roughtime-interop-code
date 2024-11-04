import sys
import os
import re
import json
import yaml
import base64
import jinja2
import logging
import datetime
import tempfile
import argparse
import subprocess
import scapy.utils
import importlib.util
from scapy.all import UDP
from argparse import ArgumentParser
from typing import Dict, List

# Kludle for loading pyroughtime from implementations folder.
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname,
        '../implementations/pyroughtime/pyroughtime/pyroughtime.py')
spec = importlib.util.spec_from_file_location('pyroughtime', filename)
pyroughtime = importlib.util.module_from_spec(spec)
sys.modules["module.name"] = pyroughtime
spec.loader.exec_module(pyroughtime)

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
    impls = args.impls['implementations']
    permutations = generate_permutations(impls)

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

    results = dict()

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

        if args.dry_run:
            logging.info('This is the bit where we pretend to run, but are not!')
            continue

        # Let's run (away from all our problems)
        perm_process = subprocess.Popen(perm_cmd.split(' '), env=env)
        try:
            perm_process.wait(float(args.timeout))
        except subprocess.TimeoutExpired:
            perm_process.kill()
            logger.warn(f'Terminating server: {perm["server"]} client: {perm["client"]}')
        cleanup_cmd = f'{args.container} compose -f {perm_config} down --remove-orphans'
        subprocess.run(cleanup_cmd.split(' '), env=env)

        # Gather results
        res = {
            'client': perm['client'],
            'server': perm['server']
        }

        # Read client log and try to match against success and failure regexes
        with open(os.path.join(perm_dir, 'client.log')) as f:
            res['client_log'] = f.read()
        success = failure = None
        if perm['regex_success'] is not None:
            success = re.compile(perm['regex_success']) \
                        .search(res['client_log']) is not None
        if perm['regex_failure'] is not None:
            failure = re.compile(perm['regex_failure']) \
                        .search(res['client_log']) is not None
        if success and failure:
            res['result'] = 'error'
        elif success and not failure:
            res['result'] = 'success'
        elif not success and failure:
            res['result'] = 'failure'
        else:
            res['result'] = 'unknown'

        # Read server log and pcap file.
        with open(os.path.join(perm_dir, 'server.log')) as f:
            res['server_log'] = f.read()
        with open(os.path.join(perm_dir, 'server.pcap'), 'rb') as f:
            res['pcap'] = base64.b64encode(f.read()).decode('ASCII')
        if perm['server'] not in results:
            results[perm['server']] = dict()
        results[perm['server']][perm['client']] = res

    # Create JSON file with array of results.
    flat_results = []
    for s in results:
        for c in results[s]:
            flat_results.append(results[s][c])
    with open(os.path.join(output_dir, 'result.json'), 'w') as f:
        f.write(json.dumps(flat_results, indent=2, sort_keys=True))

    # Parse results PCAP.
    for srv in results.values():
        for cli in srv.values():
            pcap_file = tempfile.NamedTemporaryFile(delete=True)
            pcap_file.write(base64.b64decode(cli['pcap']))
            pcap_file.flush()
            pcap = scapy.utils.rdpcap(pcap_file.name)
            pcap_file.close()
            cli['packets'] = []
            for p in pcap:
                if p.sport == 2002 or p.dport == 2002:
                    rp = pyroughtime.RoughtimePacket(packet=p.load)
                    cli['packets'].append(packet_tree_str(rp))

    # Render results HTML file.
    servers = [x for x in impls if impls[x]['server'] and impls[x]['enabled']]
    clients = [x for x in impls if impls[x]['client'] and impls[x]['enabled']]
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template('template_results.html')
    with open(os.path.join(output_dir, 'result.html'), 'w') as f:
        f.write(template.render(results=results,
                                servers=servers,
                                clients=clients))


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
                'client': client,
                'regex_success': impls[client].get('regex_success', None),
                'regex_failure': impls[client].get('regex_failure', None)
            })
    return permutations

def packet_tree_str(packet, indent=0):
    ret = ''
    istr = ''
    if indent > 1:
        istr = '  ' * (indent - 1)
    if isinstance(packet, pyroughtime.RoughtimePacket):
        ret += '%s%s\n' % (istr, packet.get_tag_str())
        for t in packet.get_tags():
            ret += packet_tree_str(packet.get_tag(t), indent + 1)
    elif isinstance(packet, pyroughtime.RoughtimeTag):
        vlen = packet.get_value_len()
        if vlen == 4 or vlen == 8:
            val = packet.to_int()
            val = '%d (0x%x)' % (val, val)
        else:
            val = packet.get_value_bytes().hex()
        ret += '%s%s (%3d) Val: %s\n' % (istr, packet.get_tag_str(), vlen, val)
    else:
        raise Exception('Bad tag type.')
    return ret
