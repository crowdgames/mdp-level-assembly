from random import choice
from math import inf
from .MDP import MDP

class PolicyIteration(MDP):
    def __init__(self, graph, max_iterations, policy_iter, gamma):
        super().__init__(graph)

        self.GAMMA = gamma
        self.MAX_ITERATIONS = max_iterations
        self.POLICY_ITER = policy_iter

        # create a random policy
        self.pi = {} 
        for n in self.G:
            self.pi[n] = choice(list(self.G.neighbors(n)))
            
    def update(self, playthrough):
        # NOTE: should the pi and U be reset?

        for _ in range(0, self.MAX_ITERATIONS, self.POLICY_ITER):
            # simplified policy evaluation
            for _ in range(self.POLICY_ITER):
                for n in self.G:
                    # NOTE: P will always be 1, and is removed from the calculation
                    # self.U[s] = self.R[s] + self.GAMMA * self.U[self.pi[s]]
                    R = self.G.nodes[n]['r']
                    self.set_node_meta_data(n, 'U', R + self.GAMMA * self.get_node_meta_data(n, 'U'))

            # policy improvement
            unchanged = True
            for n in self.G:
                old = self.pi[n]

                best_s = None
                best_u = -inf
                for n_p in self.G.neighbors(n):
                    u_p = self.get_node_meta_data(n_p, 'U')
                    if u_p > best_u:
                        best_s = n_p
                        best_u = u_p

                if old != best_s:
                    self.pi[n] = best_s
                    unchanged = False

            if unchanged:
                break