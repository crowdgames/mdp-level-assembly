from telnetlib import GA
from .QTable import QTable

class QLearning(QTable):
    def __init__(self, graph, gamma):
        super().__init__(graph, gamma)
        self.NAME = 'q'

    def update(self, playthrough):
        if len(playthrough) < 2:
            return
            
        n = playthrough[0][0]
        for n_1, _ in playthrough[1:]:
            N = self.get_node_meta_data(n, 'N') + 1
            self.set_node_meta_data(n, 'N', N)

            best = self.best_neighbor(n_1)

            ALPHA = (60.0/(59.0 + N))
            R = self.get_node_meta_data(n, 'r')
            A = self.G.edges[(n_1, best)]['Q']
            B = self.G.edges[(n, n_1)]['Q']
            self.G.edges[(n, n_1)]['Q'] += ALPHA*(R + self.GAMMA*A - B)

            n = n_1