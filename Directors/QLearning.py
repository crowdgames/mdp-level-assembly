from .QTable import QTable
from .Keys import *

from random import choices

class QLearning(QTable):
    def __init__(self, graph, gamma):
        super().__init__(graph, gamma, 'Q')

    def update(self, playthrough):
        if playthrough == None:
            return
            
        n = playthrough.entries[0].node_name
        for entry_1 in playthrough.entries[1:]:
            n_1 = entry_1.node_name
            best = self._best_neighbor(n_1)

            ALPHA = (60.0/(59.0 + self.get_md(n, C)))
            
            r = self.get_md(n, R)
            a = self.G.edges[(n_1, best)][Q]
            b = self.G.edges[(n, n_1)][Q]
            self.G.edges[(n, n_1)][Q] += ALPHA*(r + self.GAMMA*a - b)

            n = n_1

    def get(self, node):
        return self.epsilon_greedy_neighbor(node)
        # return self._weighted_neighbor(node)

    # def get_starting_node(self):
    #     best_n = None
    #     best_q = 0
    #     for n in self.visited:
    #         for e in self.G.out_edges(n):
    #             q = self.G.edges[e][Q]
    #             if q > best_q:
    #                 best_q = q
    #                 best_n = n

    #     return best_n

    # def get_starting_node(self):
    #     nodes = []
    #     weights = []
    #     for n in self.visited:
    #         best_q = 0
    #         for e in self.G.out_edges(n):
    #             q = self.G.edges[e][Q]
    #             if q > best_q:
    #                 best_q = q

    #         nodes.append(n)
    #         weights.append(best_q)

    #     return choices(nodes, weights=weights, k=1)[0]
