from math import inf
from .Base import Base
from .Keys import *

class Greedy(Base):
    def __init__(self, graph):
        super().__init__(graph, 'Greedy')
        self.G = graph

    def update(self, _):
        pass

    def get(self, node):
        best_n = None
        best_r = -inf

        for neighbor in self.G.neighbors(node):
            r = self.get_md(node, R) * self.get_p(node, neighbor)
            if r > best_r:
                best_r = r
                best_n = neighbor

        return best_n
