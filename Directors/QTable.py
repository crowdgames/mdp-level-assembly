from random import choices
from math import inf, exp

class QTable:
    def __init__(self, graph, gamma):
        self.G = graph
        self.GAMMA = gamma

        for e in graph.out_edges():
            # graph.edges[e]['Q'] = 1
            graph.edges[e]['Q'] = self.get_node_meta_data(e[1], 'max_r')

        for n in graph.nodes:
            graph.nodes[n]['N'] = 0

    def __best_neighbor(self, n):
        best_n = None
        best_q = -inf

        for e in self.G.out_edges(n):
            q = self.G.edges[e]['Q']
            if q > best_q:
                best_q = q
                best_n = e[1]

        return best_n

    def __weighted_neighbor(self, n):
        nodes = []
        weights = []
        for e in self.G.out_edges(n):
            nodes.append(e[1])
            weights.append(self.G.edges[e]['Q'])

        return choices(nodes, weights=weights, k=1)[0]

    def __softmax_neighbor(self, n):
        nodes = []
        weights = []
        for e in self.G.out_edges(n):
            nodes.append(e[1])
            weights.append(exp(self.G.edges[e]['Q']))

        return choices(nodes, weights=weights, k=1)[0]

    def get(self, n):
        return self.__weighted_neighbor(n)

    def get_node_meta_data(self, node, field_name):
        return self.G.nodes[node][field_name]

    def set_node_meta_data(self, node, field_name, value):
        self.G.nodes[node][field_name] = value
