from random import choices, choice, random
from math import inf, exp
from .Base import Base
from .Keys import *

class QTable(Base):
    def __init__(self, graph, gamma, name):
        super().__init__(graph, name)
        self.GAMMA = gamma

        for e in graph.out_edges():
            # graph.edges[e][Q] = 0
            graph.edges[e][Q] = self.get_md(e[1], D) 

    def _best_neighbor(self, n):
        best_n = None
        best_q = -inf

        for e in self.G.out_edges(n):
            q = self.G.edges[e][Q]
            if q > best_q:
                best_q = q
                best_n = e[1]

        return best_n

    def _weighted_neighbor(self, n):
        nodes = []
        weights = []
        for e in self.G.out_edges(n):
            nodes.append(e[1])
            weights.append(self.G.edges[e][Q])

        return choices(nodes, weights=weights, k=1)[0]

    def _softmax_neighbor(self, n):
        nodes = []
        weights = []
        for e in self.G.out_edges(n):
            nodes.append(e[1])
            weights.append(exp(self.G.edges[e][Q]))

        return choices(nodes, weights=weights, k=1)[0]

    def epsilon_greedy_neighbor(self, n):
        if random() < 0.1:
            return choice(list(self.G.neighbors(n)))

        return self._best_neighbor(n)
