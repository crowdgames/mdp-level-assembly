from random import choices
from math import inf

class QTable:
    def __init__(self, S, T, R):
        self.S = S
        self.R = R
        self.Q = {}
        self.N = {} # used for adaptive learning rate

        for s in S:
            self.N[s] = 1
            self.Q[s] = {}
            for s_p in T[s]:
                self.Q[s][s_p] = 0

    def best_neighbor(self, s):
        best_s = None
        best_u = -inf

        for new_s in self.Q[s]:
            next_u = self.Q[s][new_s]
            if next_u > best_u:
                best_u = next_u
                best_s = new_s

        return best_s, best_u

    def weighted_neighbor(self, s):
        w = [self.Q[s][n] for n in self.Q[s]]
        return choices(list(self.Q[s].keys()), weights=w, k=1)[0]

    def get_node_meta_data(self, node, field_name):
        return self.graph.nodes[node][field_name]