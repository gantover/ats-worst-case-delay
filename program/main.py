from shared import *
from network import Network
from flow import Flow


def main():
    net = Network("../test_cases/small-streams.v2.csv",
                  "../test_cases/small-topology.v2.csv")

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
