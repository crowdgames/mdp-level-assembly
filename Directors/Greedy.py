from random import choices
from math import inf

class Greedy:
    def __init__(self, graph):
        self.G = graph
        self.NAME = 'Greedy'

    def get_node_meta_data(self, node, field_name):
        return self.G.nodes[node][field_name]

    def set_node_meta_data(self, node, field_name, value):
        self.G.nodes[node][field_name] = value

    def update(self, _):
        pass

    def get(self, node):
        raise NotImplementedError('not using probability!')
        best_n = None
        best_r = -inf

        for neighbor in self.G.neighbors(node):
            r = self.G.nodes[neighbor]['r']
            if r > best_r:
                best_r = r
                best_n = neighbor

        print(best_r)
        return best_n
