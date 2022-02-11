from .QTable import QTable

class QLearning(QTable):
    def __init__(self, S, P, R, E, START):
        super().__init__(S, P, R, E, START, False)

    def update(self, playthrough):
        GAMMA = 0.9

        s = playthrough[0]
        for s_1 in playthrough[1:]:
            self.N[s] += 1

            best = self.best_neighbor(s_1)

            ALPHA = (60.0/(59.0 + self.N[s]))
            self.Q[s][s_1] += ALPHA*(self.R[s] + GAMMA*self.Q[s_1][best] - self.Q[s][s_1])
            s = s_1
