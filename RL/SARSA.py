from .QTable import QTable

class SARSA(QTable):
    def __init__(self, graph, gamma):
        super().__init__(graph, gamma)

    def update(self, playthrough):
        GAMMA = 0.9

        s = playthrough[0]
        s_1 = playthrough[1]
        for s_2 in playthrough[2:]:
            self.N[s] += 1

            ALPHA = (60.0/(59.0 + self.N[s]))
            self.Q[s][s_1] += ALPHA*(self.R[s] + GAMMA*self.Q[s_1][s_2] - self.Q[s][s_1])

            s = s_1
            s_1 = s_2