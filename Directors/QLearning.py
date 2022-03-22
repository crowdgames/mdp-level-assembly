from .QTable import QTable

class QLearning(QTable):
    def __init__(self, graph, gamma):
        super().__init__(graph, gamma)
        self.NAME = 'q'

    def update(self, playthrough):
        if len(playthrough) < 2:
            return
            
        n = playthrough[0][0]
        for entry_1 in playthrough[1:]:
            n_1 = entry_1[0]
            N = self.get_node_meta_data(n, 'N') + 1
            self.set_node_meta_data(n, 'N', N)

            best = self.best_neighbor(n_1)

            ALPHA = (60.0/(59.0 + N))
            raise NotImplementedError('multiply r by the transition probability!')
            raise NotImplementedError('original probability table should also be used!')
            
            R = self.get_node_meta_data(n, 'r')
            A = self.G.edges[(n_1, best)]['Q']
            B = self.G.edges[(n, n_1)]['Q']
            self.G.edges[(n, n_1)]['Q'] += ALPHA*(R + self.GAMMA*A - B)

            n = n_1

    def get(self, node):
        return self.weighted_neighbor(node)