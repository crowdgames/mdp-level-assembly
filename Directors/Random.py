from random import choice

class Random:
    def __init__(self, graph):
        self.G = graph
        self.NAME = 'random'

    def best_neighbor(self, node):
        return choice(list(self.G.neighbors(node)))

    def weighted_neighbor(self, node):
        return choice(list(self.G.neighbors(node)))

    def get_node_meta_data(self, node, field_name):
        return self.G.nodes[node][field_name]

    def set_node_meta_data(self, node, field_name, value):
        self.G.nodes[node][field_name] = value

    def update(self, _):
        pass

    def get(self, node):
        return choice(list(self.G.neighbors(node)))