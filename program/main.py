import argparse

from flow import Flow
from network import Network
from shared import *

arg_parser = argparse.ArgumentParser(description="Run the network simulator")
arg_parser.add_argument(
    "stream_file",
    metavar="stream_file",
    type=argparse.FileType("r"),
    help="The path to the stream file",
)
arg_parser.add_argument(
    "topology_file",
    metavar="topology_file",
    type=argparse.FileType("r"),
    help="The path to the topology file",
)


def main():
    args = arg_parser.parse_args()
    net = Network(args.stream_file, args.topology_file)

    flows = []
    for stream in net.streams.iterrows():
        flow = Flow(stream[1])
        flow.find_path(net.G)
        flows.append(flow)

    for flow in flows:
        flow.fill_nodes()

    for flow in flows:
        flow.get_total_delay()
        print(flow)


if __name__ == "__main__":
    main()
