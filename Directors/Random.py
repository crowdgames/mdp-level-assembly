from random import choice
from .Base import Base

class Random(Base):
    def __init__(self, graph):
        super().__init__(graph, 'Random')

    def update(self, _):
        pass

    def get(self, node):
        return choice(list(self.G.neighbors(node)))

    def get_starting_node(self):
        raise NotImplementedError('Caller must implement the "get_starting_node" method.')

    def get_starting_node(self):
        return choice(list(self.visited))