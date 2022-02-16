from .MDP import MDP

class ValueIteration(MDP):
    def __init__(self, graph, max_iterations, gamma, theta):
        super().__init__(graph)
        self.THETA = theta

        self.MAX_ITERATIONS = max_iterations
        self.GAMMA = gamma
        self.MIN_N = 10
        self.R_PLUS = 100

    def update(self, _):
        # Something like this may allow for better adaptability to new players
        # self.R_PLUS += 5
        # self.MIN_N += 5

        # NOTE: should U be reset?
        # NOTE: implementation is in-place value iteration
        for n in self.G.nodes:
            self.G.nodes[n]['U'] = 1

        for _ in range(self.MAX_ITERATIONS):
            delta = 0

            for n in self.G:
                self.G.nodes[n]['N'] += 1
                N = self.G.nodes[n]['N']
                if N < self.MIN_N:
                    u = self.R_PLUS - N
                else:
                    # NOTE: P will always be 1, and is removed from the calculation
                    R = self.G.nodes[n]['U']
                    u = R + self.GAMMA * max(self.G.nodes[n_p]['U'] for n_p in self.G.neighbors(n))
                
                delta = max(delta, abs(self.G.nodes[n]['U'] - u))
                self.G.nodes[n]['U'] = u

            # if delta < self.THETA:
            #     break
