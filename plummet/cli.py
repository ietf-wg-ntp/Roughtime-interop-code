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
    parser = ArgumentParser(description=CMD_INFO)
    parser.add_argument('-i', help='')
    parser.parse_args()


# For each implementation that we know of, based on it having a client and/or
# server, work out permutations of all.
def generate_permutations():
    pass