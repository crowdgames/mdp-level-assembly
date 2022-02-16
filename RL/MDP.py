from math import inf
from random import choices

class MDP:
    def __init__(self, graph):
        self.G = graph
        for n in graph.nodes:
            graph.nodes[n]['U'] = 0
            graph.nodes[n]['N'] = 0

    def best_neighbor(self, node):
        best_s = None
        best_u = -inf

        for new_s in self.T[s]:
            next_u = self.U[new_s]
            if next_u > best_u:
                best_u = next_u
                best_s = new_s

        return best_s

    def weighted_neighbor(self, node):
        n = []
        w = []

        for neighbor in self.G.neighbors(node):
            n.append(neighbor)
            w.append(self.G.nodes[neighbor]['U'])

        return choices(n, weights=w, k=1)[0]

    def get_node_meta_data(self, node, field_name):
        return self.G.nodes[node][field_name]

    def update_node_meta_data(self, node, field_name, value):
        self.G.nodes[node][field_name] = value
        
