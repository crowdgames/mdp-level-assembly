from telnetlib import GA
from .QTable import QTable

class QLearning(QTable):
    def __init__(self, graph, gamma):
        super().__init__(graph, gamma)

    def update(self, playthrough):
        n = playthrough[0][0]
        for n_1, _ in playthrough[1:]:
            # self.Q[s][s_1] += ALPHA*(self.R[s] + GAMMA*self.Q[s_1][best] - self.Q[s][s_1])
            N = self.get_node_meta_data(n, 'N') + 1
            self.set_node_meta_data(n, 'N', N)

            best = self.best_neighbor(n_1)

            ALPHA = (60.0/(59.0 + N))
            R = self.get_node_meta_data(n, 'r')
            a = self.G.edges[(n_1, best)]['Q']
            b = self.G.edges[(n, n_1)]['Q']
            self.G.edges[(n, n_1)]['Q'] += ALPHA*(R + self.GAMMA*a - b)

            n = n_1