from .Keys import *

class Base:
    def __init__(self, graph, name):
        self.G = graph
        self.NAME = name

    def get(self, node):
        raise NotImplementedError('Caller must implement the "get" method.')

    def update(self, playthrough):
        raise NotImplementedError('Caller must implement the "update" method.')

    def get_p(self, cur_n, next_n):
        numerator = self.get_md(next_n, C) * self.get_md(next_n, PD)
        total = numerator

        for n in self.G.neighbors(cur_n):
            total +=  self.get_md(n, C) * self.get_md(n, PD)

        return numerator / total

    def increment_count(self, node):
        self.G.nodes[node][C] += 1

    def get_md(self, node, field_name):
        # get node meta data
        return self.G.nodes[node][field_name]

    def set_md(self, node, field_name, value):
        # set meta data
        self.G.nodes[node][field_name] = value