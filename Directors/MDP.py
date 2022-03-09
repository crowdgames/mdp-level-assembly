from math import inf
from random import choices
from math import exp

class MDP:
    def __init__(self, graph):
        self.G = graph
        for n in graph.nodes:
            graph.nodes[n]['U'] = 0
            graph.nodes[n]['N'] = 0

    def best_neighbor(self, node):
        best_n = None
        best_u = -inf

        for neighbor in self.G.neighbors(node):
            u = self.G.nodes[neighbor]['U']
            if u > best_u:
                best_u = u
                best_n = neighbor

        return best_n

    def weighted_neighbor(self, node):
        n = []
        w = []

        for neighbor in self.G.neighbors(node):
            n.append(neighbor)
            w.append(self.G.nodes[neighbor]['U'])

        offset = min(w) 
        if offset < 0:
            w = [a-offset+0.1 for a in w]

        return choices(n, weights=w, k=1)[0]

    def softmax_neighbor(self, node):
        n = []
        w = []

        for neighbor in self.G.neighbors(node):
            n.append(neighbor)
            w.append(exp(self.G.nodes[neighbor]['U']))

        return choices(n, weights=w, k=1)[0]

    def get_node_meta_data(self, node, field_name):
        return self.G.nodes[node][field_name]

    def set_node_meta_data(self, node, field_name, value):
        self.G.nodes[node][field_name] = value
        
