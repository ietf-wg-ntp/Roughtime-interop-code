import sys
import yaml
import logging
import argparse
from argparse import ArgumentParser

CMD_INFO = """
plummet takes all the known roughtime implementations and attempts to perform
interop tests against each client/server pair.
"""

# Load the JSON file with the list of servers and clients
# Make a list of permutations
# Run Docker

# TODO: How to get packet captures
# TODO: Work out output directories
# TODO: Packet Capture
# TODO: Work out serving results - HTML?

def main() -> None:
    logger = logging.getLogger('plummet')

    parser = ArgumentParser(description=CMD_INFO)
    parser.add_argument('--impls', type=argparse.FileType('r'),
                        default='implementations/implementations.yml',
                        help='Path to the implementations YAML file')
    parser.add_argument('--dry-run', action=argparse.BooleanOptionalAction,
                        help="Don't make any system calls, just print")
    args = parser.parse_args()
    try:
        args.impls = yaml.safe_load(args.impls.read())
    except yaml.YAMLError as e:
        logger.critical('Implementations YAML appaers bad, exiting...')
        sys.exit(1)


# For each implementation that we know of, based on it having a client and/or
# server, work out permutations of all.
def generate_permutations():
    pass