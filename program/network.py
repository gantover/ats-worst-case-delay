from shared import *
import networkx as nx
import pandas as pd

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
    
        self.G = nx.MultiGraph()

        for link in self.links.iterrows():
            source = link[1]['SourceDevice']
            destination = link[1]['DestinationDevice']
            source_port = link[1]['SourcePort']
            link_id = link[1]['LinkID']
            destination_port = link[1]['DestinationPort']
            self.G.add_edge(source,
                   destination,
                   source_port=source_port,
                   destination_port=destination_port,
                   link_id=link_id,
                   flows=dict() # priority: flow
                  )
    
        for end_system in self.end_systems.iterrows():
            # the names are supposedly already inside the graph because of the link creation
            name = end_system[1]['DeviceName']
            self.G.nodes[name]['ports'] = end_system[1]['Ports']
    
        for switch in self.switches.iterrows():
            name = switch[1]['DeviceName']
            self.G.nodes[name]['ports'] = switch[1]['Ports']
