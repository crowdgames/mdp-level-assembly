from math import inf
from random import choices

class MDP:
    def __init__(self, S, T, R):
        self.S = S
        self.T = T
        self.R = R
        self.U = {}

        for s in S:
            self.U[s] = 0

    def best_neighbor(self, s):
        best_s = None
        best_u = -inf

        for new_s in self.T[s]:
            next_u = self.U[new_s]
            if next_u > best_u:
                best_u = next_u
                best_s = new_s

        return best_s

    def weighted_neighbor(self, s):
        w = [self.U[n] for n in self.T[s]]
        return choices(self.T[s], weights=w, k=1)[0]
