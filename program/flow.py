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
        self.total_delay = None
    
    def find_path(self, G: nx.MultiGraph):
        # first we find the shortest path from the source to the destination of the stream 
        path = nx.shortest_path(G, self.src, self.dest) 
        self.path = path
        graph = nx.path_graph(path)
        edges = graph.edges()
        self.links = []
        for edge in edges:
            link = G.edges.get([edge[0], edge[1], 0])
            self.links.append({"edges": [G.nodes[edge[0]], G.nodes[edge[1]]], "data": link})

    def __repr__(self):
        # just to have a print for comparison with solution.csv file
        path = "->".join(self.path)
        return f"{self.name},{round(self.total_delay * 1e6, 3)},{self.deadline},{path}"

    def fill_nodes(self):
        # takes each nodes and adds this flow to the array
        # of all flows going through
        for link in self.links:
            link_flows = link["data"]["flows"]
            link_flows[self.priority] = [*link_flows.get(self.priority, []), self]

    def hop_delay(self, link, next_link = None):
        bH = 0
        rH = 0
        for priority in range(self.priority+1, MAX_PRIORITY+1):
            for flow in link["data"]["flows"].get(priority, []):
                bH += flow.b
                rH += flow.r
        lL = 0
        for priority in range(0, self.priority):
            for flow in link["data"]["flows"].get(priority, []):
                if flow.l > lL:
                    lL = flow.l
        

        shaped_queue_flows = []
        for flow in link["data"]["flows"][self.priority]:
            if next_link:
                if not (flow in next_link["data"]["flows"][self.priority]):
                    # we have to have the same output port on the switch
                    continue
            shaped_queue_flows.append(flow)
            
        max_delay = 0
        for flow in shaped_queue_flows:
            bc = 0
            for bc_flow in shaped_queue_flows:
                if bc_flow != flow:
                    bc += bc_flow.b
            lj = flow.l
            delay = (bH + bc + lL) / (RATE - rH) + lj / RATE
            if delay > max_delay:
                max_delay = delay
        
        return max_delay

    def get_total_delay(self):
        total = 0
        for i in range(len(self.links)-1):
            total += self.hop_delay(self.links[i], self.links[i+1])
        total += self.hop_delay(self.links[-1], None)
        self.total_delay = total
