import networkx as nx

def Create_Graph_old(end_systems,switches, links):
    """Older and longer implementation"""
    G= nx.MultiGraph()
    # multi graph to allow multiple links between two same nodes

    # this creates the links as well as the necessary nodes
    for link in links.iterrows():
        source = link[1]['SourceDevice']
        destination = link[1]['DestinationDevice']
        source_port = link[1]['SourcePort']
        link_id = link[1]['LinkID']
        destination_port = link[1]['DestinationPort']
        G.add_edge(source,
                destination,
                source_port=source_port,
                destination_port=destination_port,
                link_id=link_id,
                flows=dict() # priority: flow
                )

    for end_system in end_systems.iterrows():
        # the names are supposedly already inside the graph because of the link creation
        name = end_system[1]['DeviceName']
        G.nodes[name]['ports'] = end_system[1]['Ports']
        G.nodes[name]['input_flows'] = dict()
        G.nodes[name]['output_flows'] = dict()

    for switch in switches.iterrows():
        name = switch[1]['DeviceName']
        G.nodes[name]['ports'] = switch[1]['Ports']
        G.nodes[name]['input_flows'] = dict()
        G.nodes[name]['output_flows'] = dict()
        
    return G

def Create_graph(devices, links) -> nx.Graph:
    """constructs a graph"""
    G = nx.Graph()
    # Add devices as nodes with type attribute
    for device in devices.iterrows():
        device_type, device_name, _ = device[1]
        G.add_node(device_name, type=device_type)
    # Add links as edges
    for link in links.iterrows():
        # LINK, link_id, node1, port1, node2, port2
        _, _, node1, _, node2, _ = link[1]
        G.add_edge(node1, node2)
        
    return G