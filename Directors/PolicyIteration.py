from random import choice
from math import inf
from .MDP import MDP
from .Keys import *

class PolicyIteration(MDP):
    def __init__(self, graph, max_iterations, policy_iter, gamma):
        super().__init__(graph, 'Policy')

        self.GAMMA = gamma
        self.MAX_ITERATIONS = max_iterations
        self.POLICY_ITER = policy_iter
            
    def update(self, _):
        # create a random policy
        self.pi = {} 
        for n in self.G:
            self.pi[n] = choice(list(self.G.neighbors(n)))

        # all utility values are reset to 0. Note, in time-sensitive computations
        # this could be only done every once in a while, but this hasn't been an
        # issue in our use case since the graphs we use are not large enough. It 
        # takes less than half a second to converge, and this isn't an optimized
        # implementation and, after all, this is Python.
        self._reset_utility()

        # run policy iteration
        for _ in range(0, self.MAX_ITERATIONS, self.POLICY_ITER):
            # simplified policy evaluation
            for _ in range(self.POLICY_ITER):
                for n in self.G:
                    # reward for current node
                    r = self.G.nodes[n][R] 
                    # target node according to policy
                    n_p = self.pi[n] 
                    # Utility of the node found by the policy
                    u_p = self.get_md(n_p, U)
                    # the probability of the node found by the policy being selected
                    p = self.get_p(n, n_p)
                    # Updated utility of the current node
                    self.set_md(n, 'U', r + self.GAMMA * p * u_p)

            # policy improvement
            unchanged = True
            for n in self.G:
                old = self.pi[n]

                best_s = None
                best_u = -inf
                for n_p in self.G.neighbors(n):
                    u_p = self.get_md(n_p, U) * self.get_p(n, n_p)
                    if u_p > best_u:
                        best_s = n_p
                        best_u = u_p

                if old != best_s:
                    self.pi[n] = best_s
                    unchanged = False

            if unchanged:
                break

    def get(self, node):
        return self._best_neighbor(node)