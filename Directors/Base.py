from .Keys import *
import networkx as nx

class Base:
    def __init__(self, graph, name):
        self.G = graph
        self.NAME = name

        # reset everything to just be redundant
        for n in self.G.nodes:
            self.G.nodes[n][C] = 1
            self.G.nodes[n][U] = 0 # redundant
            self.G.nodes[n][R] = self.G.nodes[n][D]

        self.visited = set()

    def get(self, node):
        raise NotImplementedError('Caller must implement the "get" method.')

    def get_starting_node(self):
        raise NotImplementedError('Caller must implement the "get_starting_node" method.')

    def update(self, playthrough):
        raise NotImplementedError('Caller must implement the "update" method.')

    def increment_count(self, node):
        self.G.nodes[node][C] += 1

    def get_md(self, node, field_name):
        # get node meta data
        return self.G.nodes[node][field_name]

    def set_md(self, node, field_name, value):
        # set node meta data
        self.G.nodes[node][field_name] = value