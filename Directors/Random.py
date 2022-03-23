from random import choice
from .Base import Base

class Random(Base):
    def __init__(self, graph):
        super().__init__(graph, 'Random')

    def update(self, _):
        pass

    def get(self, node):
        return choice(list(self.G.neighbors(node)))