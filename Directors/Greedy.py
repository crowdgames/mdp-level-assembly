from math import inf
from .Base import Base
from .Keys import *

class Greedy(Base):
    def __init__(self, graph):
        super().__init__(graph, 'Greedy')

    def update(self, _):
        pass

    def get(self, node):
        best_n = None
        best_r = -inf

        for neighbor in self.G.neighbors(node):
            r = self.get_md((neighbor), R)
            if r > best_r:
                best_r = r
                best_n = neighbor

        return best_n

    def get_starting_node(self):
        best_n = None
        best_r = 0
        for n in self.visited:
            r = self.get_md(n, R)
            if r > best_r:
                best_r = r
                best_n = n

        return best_n

