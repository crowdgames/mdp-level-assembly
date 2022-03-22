from random import choice
from math import inf
from .MDP import MDP

class PolicyIteration(MDP):
    def __init__(self, graph, max_iterations, policy_iter, gamma):
        super().__init__(graph)

        self.GAMMA = gamma
        self.MAX_ITERATIONS = max_iterations
        self.POLICY_ITER = policy_iter
        self.NAME = 'policy'
            
    def update(self, _):
        # create a random policy and reset utility to 0
        self.pi = {} 
        for n in self.G:
            self.pi[n] = choice(list(self.G.neighbors(n)))

        for n in self.G.nodes:
            self.G.nodes[n]['U'] = 0

        for _ in range(0, self.MAX_ITERATIONS, self.POLICY_ITER):
            # simplified policy evaluation
            for _ in range(self.POLICY_ITER):
                for n in self.G:
                    # reward for current node
                    R = self.G.nodes[n]['r'] 
                    # target node according to policy
                    N_p = self.pi[n] 
                    # Utility of the node found by the policy
                    U_p = self.get_node_meta_data(N_p, 'U')
                    # the probability of the node found by the policy being selected
                    P = self.G.nodes[n]['P'][N_p]
                    # Updated utility of the current node
                    self.set_node_meta_data(n, 'U', R + self.GAMMA * P * U_p)

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

    def get(self, node):
        return self._best_neighbor(node)