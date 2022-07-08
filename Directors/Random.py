from random import choice
from .Base import Base

class Random(Base):
    def __init__(self, graph):
        super().__init__(graph, 'Random')

    def update(self, _):
        pass

    def get(self, node, k):
        nodes = [node]
        size = 1
        while size < k:
            node = choice(list(self.G.neighbors(node)))
            nodes.append(node)
            size += 1 * '__' not in node # small optimization to remove branching

        return nodes

    def get_starting_node(self):
        return choice(list(self.visited_iter()))