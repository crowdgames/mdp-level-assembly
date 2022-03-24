from .QTable import QTable
from .Keys import *

class SARSA(QTable):
    def __init__(self, graph, gamma):
        super().__init__(graph, gamma, 'SARSA')

    def update(self, playthrough):
        raise NotImplementedError('Outdated implementation. Use q-learning as a reference.')
        if len(playthrough) < 3:
            return

        n = playthrough[0][0]
        n_1 = playthrough[1][0]
        for n_2, _, _, _ in playthrough[2:]:
            R = self.get_node_meta_data(n, 'r')
            ALPHA = (60.0/(59.0 + self.get_md(n, C)))
            A = self.G.edges[n_1, n_2][Q] 
            B = self.G.edges[n, n_1][Q]

            self.G.edges[n, n_1][Q] += ALPHA*(R + self.GAMMA*A - B)

            n = n_1
            n_1 = n_2

    def get(self, node):
        return self.weighted_neighbor(node)