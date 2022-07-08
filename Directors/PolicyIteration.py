from random import choice, choices
from math import inf
from .MDP import MDP
from .Keys import *

from networkx import set_node_attributes

class PolicyIteration(MDP):
    def __init__(self, graph, max_iterations, policy_iter, gamma):
        super().__init__(graph, 'Policy')

        self.GAMMA = gamma
        self.MAX_ITERATIONS = max_iterations
        self.POLICY_ITER = policy_iter

    def __get_u(self, n):
        # Regular
        return self.get_md(n, U)
        
        # GLIE
        # if self.get_md(n, C) >= 2:
        #     return self.get_md(n, U)
        # return 2 + self.get_md(n, U)

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
        # from tqdm import tqdm
        # from time import time
        # start = time()
        # bar = tqdm()
        # i = 0
        # while start + 0.6 > time():
        while True:
            # __num_changes = 0

            # policy evaluation
            for __ in range(self.POLICY_ITER):
                # u_temp = {}
                for n in self.G:
                    r = self.get_md(n, R) 
                    # n_p = n
                    # for _ in range(4):
                    #     n_p = self.pi[n_p]
                    # u = self.__get_u(n_p)
                    u = self.__get_u(self.pi[n])
                    # u = max(self.__get_u(n_p) for n_p in self.G.neighbors(n)) 
                    self.set_md(n, U, r + self.GAMMA*u)
                    # u_temp[n] = {U: r + self.GAMMA*u}
                
                # set_node_attributes(self.G, u_temp)
            
            # policy improvement
            changed = False
            for n in self.G:
                old = self.pi[n]

                best_s = None
                best_u = -inf
                for n_p in self.G.neighbors(n):
                    u_p = self.__get_u(n_p)
                    if u_p > best_u:
                        best_s = n_p
                        best_u = u_p

                if old != best_s:
                    # __num_changes += 1
                    self.pi[n] = best_s
                    changed = True

            # bar.set_description(f'num changes: {__num_changes}')

            if not changed:
                break
            
    def get(self, node, k):
        # def __p(k):
        #     print(k)
        #     print(f'\tC: {self.get_md(k, C)}')
        #     print(f'\tU: {self.get_md(k, U)}')
        #     print(f'\tR: {self.get_md(k, R)}')

        #     for n in self.G.neighbors(k):
        #         print(f'\t\t{n} :: {self.pi[k] == n}\t:: R={self.get_md(n, R):.5f} :: U={self.get_md(n, U):.5f}')

        # print(f'{node} -> {self.pi[node]}')
        # __p(node)
        # print()

        nodes = [node]
        size = 1
        while size < k:
            node = self.pi[node]
            nodes.append(node)
            size += 1 * '__' not in node # small optimization to remove branching

        return nodes

    def get_starting_node(self):
        nodes = list(self.visited_iter())
        weights = [self.__get_u(n) for n in nodes]
        return choices(nodes, weights=weights, k=1)[0]
