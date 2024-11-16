from shared import *
from network import Network
from flow import Flow


def main():
    net = Network("../simulation_files/little/streams.csv",
                  "../simulation_files/little/topology.csv")

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

    # for flow in flows:
    #     flow.new_get_total_delay()
    #     print(flow)

if __name__ == "__main__":
    main()
