from math import inf
from random import choices, random, choice
from math import exp

from .Base import Base
from .Keys import *

class MDP(Base):
    def __init__(self, graph, name):
        super().__init__(graph, name)
        self._reset_utility()

    def _reset_utility(self):
        for n in self.G.nodes:
            self.G.nodes[n][U] = 0

    def _best_neighbor(self, node):
        best_n = None
        best_u = -inf

        for neighbor in self.G.neighbors(node):
            new_u = self.get_md(neighbor, U)

            if new_u > best_u:
                best_u = new_u
                best_n = neighbor

        return best_n

    def _weighted_neighbor(self, node):
        n = []
        w = []

        for neighbor in self.G.neighbors(node):
            n.append(neighbor)
            w.append(self.get_md(neighbor, U))

        offset = min(w) 
        if offset < 0:
            w = [a-offset+0.1 for a in w]

        return choices(n, weights=w, k=1)[0]

    def _softmax_neighbor(self, node):
        n = []
        w = []

        for neighbor in self.G.neighbors(node):
            n.append(neighbor)
            w.append(exp(self.get_md(neighbor, U)))

        return choices(n, weights=w, k=1)[0]

    def _epsilon_greedy_neighbor(self, node):
        if random() < 0.1:
            return choice(list(self.G.neighbors(node)))

        return self._epsilon_greedy_neighbor(node)
        # return self._best_neighbor(node)

        

        
