from shared import *

class Flow():
    def __init__(self, data_row):
        # filling a class for each stream to manipulate the data more easily
        self.priority = data_row["PCP"]
        self.src = data_row["SourceNode"]
        self.dest = data_row["DestinationNode"]
        self.b = data_row["Size"]
        self.r = data_row["Size"] / data_row["Period"]
        self.deadline = data_row["Deadline"]
        self.name = data_row["StreamName"]
        self.l = data_row["Size"] # packet length
        self.total_delay = 0 
    
    def find_path(self, G: nx.Graph):
        # first we find the shortest path from the source to the destination of the stream 
        path = nx.shortest_path(G, self.src, self.dest) 
        self.path = path
        graph = nx.path_graph(path)
        edges = graph.edges()
        self.links = []
        for edge in edges:
            link = G.edges.get([edge[0], edge[1]])
            assert link != None
            src_port = int(link["src_port"])
            dest_port = int(link["dest_port"])
            if link["src"] == edge[1] and link["dest"] == edge[0]:
                temp = src_port
                src_port = dest_port
                dest_port = temp
            self.links.append({"nodes": [G.nodes[edge[0]], G.nodes[edge[1]]], "src_port": src_port, "dest_port": dest_port})

    def __repr__(self):
        # just to have a print for comparison with solution.csv file
        path = "->".join(self.path)
        return f"{self.name},{round(self.total_delay * 1e6, 3)},{self.deadline},{path}"

    def fill_nodes(self):
        # takes each nodes and adds this flow to the array
        # of all flows going through
        
        # for the ES sending the message, since there is only one port
        # there is only one egress and one ingress : 0
        node, _ = self.links[0]["nodes"]
        node_sq = node["egress"][1]["shaped_queues"]
        node_sq[self.priority] = node_sq.get(self.priority, dict())
        node_sq[self.priority][1] = node_sq[self.priority].get(1, [])
        node_sq[self.priority][1].append(self)

        for i in range(1,len(self.links)):
            # we take the links that surround our edge (ES or SW) of interest
            link_prev = self.links[i-1]
            link_next = self.links[i]
            # we take the ports our flow will go through
            egress_port = link_next["src_port"]
            ingress_port = link_prev["dest_port"]
            _, node0 = link_prev["nodes"]
            node1, _ = link_next["nodes"]
            assert node0 == node1
            node = node0
            node_sq = node["egress"][egress_port]["shaped_queues"]
            node_sq[self.priority] = node_sq.get(self.priority, dict())
            node_sq[self.priority][ingress_port] = node_sq[self.priority].get(ingress_port, [])
            node_sq[self.priority][ingress_port].append(self)

    def hop_delay(self, node, ingress, egress):
        bH, rH, lL = 0, 0, 0
        for priority in range(self.priority+1, MAX_PRIORITY+1):
            for flow in node["egress"][egress]["ready_queues"].get(priority):
                bH += flow.b
                rH += flow.r
        for priority in range(0, self.priority):
            for flow in node["egress"][egress]["ready_queues"].get(priority): 
                lL = max(flow.l, lL)
        

        shaped_queue = node["egress"][egress]["shaped_queues"][self.priority][ingress]

        max_delay = 0
        for flow in shaped_queue:
            bc = 0
            for bc_flow in shaped_queue:
                if bc_flow != flow:
                    bc += bc_flow.b
            lj = flow.l
            delay = (bH + bc + lL) / (RATE - rH) + lj / RATE
            max_delay = max(delay, max_delay)

        return max_delay
            
    def get_total_delay(self):
        total = 0
        node, _ = self.links[0]["nodes"]
        total += self.hop_delay(node, 1, 1)
        for i in range(1, len(self.links)):
            ingress = self.links[i-1]["dest_port"]
            egress = self.links[i]["src_port"]
            _, node = self.links[i-1]["nodes"]
            total += self.hop_delay(node, ingress, egress)

        self.total_delay = total
