from random import choice, choices
from math import inf
from .MDP import MDP
from .Keys import *

class PolicyIteration(MDP):
    def __init__(self, graph, max_iterations, policy_iter, gamma):
        super().__init__(graph, 'Policy')

        self.GAMMA = gamma
        self.MAX_ITERATIONS = max_iterations
        self.POLICY_ITER = policy_iter

    def __get_u(self, n):
        return self.get_md(self.pi[n], U)
        # if self.get_md(n, C) >= 2:
        #     return self.get_md(self.pi[n], U)

        # return 2 + self.get_md(self.pi[n], U)
        # return 2

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
        i = 0
        while True:
            # policy evaluation
            for __ in range(self.POLICY_ITER):
                for n in self.G:
                    r = self.get_md(n, R)
                    max_u = max(self.get_md(n_p, U) for n_p in self.G.neighbors(n))
                    self.set_md(n, U, r + self.GAMMA * max_u)
                    # r = self.get_md(n, R)
                    # u = r + self.GAMMA*self.get_md(self.pi[n], U) 
                    # self.set_md(n, U, u)
            
            # policy improvement
            changed = False
            for n in self.G:
                old = self.pi[n]

                best_s = None
                best_u = -inf
                for n_p in self.G.neighbors(n):
                    u_p = self.get_md(n_p, U) 
                    if u_p > best_u:
                        best_s = n_p
                        best_u = u_p

                if old != best_s:
                    self.pi[n] = best_s
                    changed = True
            
            i += 1 
            if not changed:
                break
            
        print()
        print(f'\n{i} iterations to converge\n')
        def __p(k):
            print(k)
            print(f'\tC: {self.get_md(k, C)}')
            print(f'\tU: {self.get_md(k, U)}')
            print(f'\tR: {self.get_md(k, R)}')

            for n in self.G.neighbors(k):
                print(f'\t\t{n} :: {self.pi[k] == n} :: {self.get_md(n, R)} :: {self.get_md(n, U)}')

        for k in self.visited_iter():
            __p(k)

        print()

    def get(self, node):
        print(f'{node} -> {self.pi[node]}')
        return self.pi[node]
