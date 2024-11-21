from shared import *

class ReadyQueues():
    def __init__(self, shaped_queues):
        self.sq = shaped_queues
    def get(self, name):
        sq = list(self.sq.get(name, dict()).values())
        returned = []
        for ingress in sq:
            returned = [*returned, *ingress]
        return returned

ShapedQueues = dict

class Network:
    def __init__(self, stream_file: str, topology_file: str):
        self.streams = pd.read_csv(stream_file,
                                   names=['PCP','StreamName','StreamType','SourceNode','DestinationNode','Size','Period','Deadline'])
        topology_cols = [str(i) for i in range(7)]
        self.topology = pd.read_csv(topology_file,names=topology_cols).groupby('0')
    
        self.switches = self.topology.get_group('SW')
        self.switches = self.switches.drop(columns=['4','5','6'])
        self.switches.columns = ['DeviceType','DeviceName','Ports','Domain']
   
        self.end_systems = self.topology.get_group('ES')
        self.end_systems = self.end_systems.drop(columns=['4','5','6'])
        self.end_systems.columns = ['DeviceType','DeviceName','Ports','Domain']
    
        self.links = self.topology.get_group('LINK')
        self.links.columns = ['LINK','LinkID','SourceDevice','SourcePort','DestinationDevice','DestinationPort','Domain']
    
        self.G = nx.Graph()

        for link in self.links.iterrows():
            source = link[1]['SourceDevice']
            destination = link[1]['DestinationDevice']
            src_port = link[1]['SourcePort']
            link_id = link[1]['LinkID']
            dest_port = link[1]['DestinationPort']
            self.G.add_edge(source,
                            destination,
                            src=source,
                            dest=destination,
                            src_port=src_port,
                            dest_port=dest_port,
                            link_id=link_id,
                            )
    
        # the names of ES and SW are supposedly already inside the graph because of the link creation
        for end_system in self.end_systems.iterrows():
            name = end_system[1]['DeviceName']
            self.G.nodes[name]['ports'] = end_system[1]['Ports']
            num_ports = int(end_system[1]['Ports'])
            assert (num_ports == 1)
            self.G.nodes[name]['egress'] = {port : dict() for port in range(num_ports)}

            for port in range(num_ports):
                shaped_queues = ShapedQueues()
                self.G.nodes[name]['egress'][port]["shaped_queues"] = shaped_queues
                self.G.nodes[name]['egress'][port]["ready_queues"] = ReadyQueues(shaped_queues) 
    
        for switch in self.switches.iterrows():
            name = switch[1]['DeviceName']
            self.G.nodes[name]['ports'] = switch[1]['Ports']
            num_ports = int(switch[1]['Ports'])
            assert (num_ports > 1 and num_ports <= 8)
            self.G.nodes[name]['egress'] = {port : dict() for port in range(num_ports)}

            for port in range(num_ports):
                shaped_queues = ShapedQueues()
                self.G.nodes[name]['egress'][port]["shaped_queues"] = shaped_queues
                self.G.nodes[name]['egress'][port]["ready_queues"] = ReadyQueues(shaped_queues) 
