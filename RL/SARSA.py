from .QTable import QTable

class SARSA(QTable):
    def __init__(self, graph, gamma):
        super().__init__(graph, gamma)

    def update(self, playthrough):
        n = playthrough[0][0]
        n_1 = playthrough[1][0]
        for n_2, _ in playthrough[2:]:
            N = self.get_node_meta_data(n, 'N') + 1
            self.set_node_meta_data(n, 'N', N)

            R = self.get_node_meta_data(n, 'r')
            ALPHA = (60.0/(59.0 + N))
            A = self.G.edges[n_1, n_2]['Q'] 
            B = self.G.edges[n, n_1]['Q']

            self.G.edges[n, n_1]['Q'] += ALPHA*(R + self.GAMMA*A - B)

            n = n_1
            n_1 = n_2