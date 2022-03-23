from .QTable import QTable
from .Keys import *

class QLearning(QTable):
    def __init__(self, graph, gamma):
        super().__init__(graph, gamma, 'Q')

    def update(self, playthrough):
        if len(playthrough) < 2:
            return
            
        n = playthrough[0][0]
        for entry_1 in playthrough[1:]:
            n_1 = entry_1[0]
            best = self._best_neighbor(n_1)

            ALPHA = (60.0/(59.0 + self.get_md(n, C)))
            
            R = self.get_node_meta_data(n, R)
            A = self.G.edges[(n_1, best)][Q]*self.get_p(n_1, best)
            B = self.G.edges[(n, n_1)][Q]*self.get_p(n, n_1)
            self.G.edges[(n, n_1)][Q] += ALPHA*(R + self.GAMMA*A - B)

            n = n_1

    def get(self, node):
        return self._weighted_neighbor(node)