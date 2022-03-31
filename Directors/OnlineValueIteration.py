from email.policy import Policy
from random import choice
from math import inf

from Directors.PolicyIteration import PolicyIteration
from .MDP import MDP
from .Keys import *

class OnlineValueIteration(MDP):
    def __init__(self, graph, gamma):
        super().__init__(graph, 'Online Value Iteration')

        self.GAMMA = gamma

    def f(self, n, count):
        if count >= 1:
            return 2
        
        return max(self.get_md(n_p, U) for n_p in self.G.neighbors(n))

    def update(self, playthrough):
        for k in range(20):
            # for entry in playthrough.entries:
            for n in self.G:
                # n = entry.node_name
                c = self.get_md(n, C)
                r = self.get_md(n, R)

                self.set_md(n, 'U', r + self.GAMMA*self.f(n, c))

    def get(self, node):
        # return self._best_neighbor(node)
        return self._epsilon_greedy_neighbor(node)