from .MDP import MDP
from .Keys import *

class ValueIteration(MDP):
    def __init__(self, graph, max_iterations, gamma, theta):
        super().__init__(graph, 'Value')
        self.THETA = theta

        self.MAX_ITERATIONS = max_iterations
        self.GAMMA = gamma
        self.MIN_N = 10
        self.R_PLUS = 100

    def update(self, _):
        # NOTE: implementation is in-place value iteration
        for n in self.G.nodes:
            self.G.nodes[n]['U'] = 0

        for _ in range(self.MAX_ITERATIONS):
            delta = 0

            for n in self.G:
                R = self.G.nodes[n]['r']
                u = R + self.GAMMA * max(self.G.nodes[n_p][U] for n_p in self.G.neighbors(n))
                
                delta = max(delta, abs(self.G.nodes[n][U] - u))
                self.G.nodes[n][U] = u

            # if delta < self.THETA:
            #     break

    def get(self, node):
        # return self._best_neighbor(node)
        return self._epsilon_greedy_neighbor(node)

    # def get_starting_node(self):
    #     raise NotImplementedError('Caller must implement the "get_starting_node" method.')