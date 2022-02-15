from random import choice
from math import inf
from .MDP import MDP

class PolicyIteration(MDP):
    def __init__(self, graph, gamma):
        super().__init__(graph)

        self.GAMMA = gamma

        # create a random policy
        self.pi = {} 
        for s in S:
            self.pi[s] = choice(list(self.P[s].keys()))
            
    def update(self, playthrough, max_iterations=1_000):
        ITER = 20

        # NOTE: should the pi and U be reset?

        for i in range(0, max_iterations, ITER):
            # simplified policy evaluation
            for _ in range(ITER):
                for s in self.S:
                    # NOTE: P will always be 1, and is removed from the calculation
                    self.U[s] = self.R[s] + self.GAMMA * self.U[self.pi[s]]

            # policy improvement
            unchanged = True
            for s in self.S:
                old = self.pi[s]

                best_s = None
                best_u = -inf
                for s_p in self.P[s]:
                    if self.U[s_p] > best_u:
                        best_s = s_p
                        best_u = self.U[s_p]

                if old != best_s:
                    self.pi[s] = best_s
                    unchanged = False

            if unchanged:
                break