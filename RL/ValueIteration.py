from .MDP import MDP

class ValueIteration(MDP):
    def __init__(self, S, T, R, theta):
        super().__init__(S, T, R)
        self.theta = theta
        self.N = {}
        for s in self.S:
            self.N[s] = 0

        self.GAMMA = 0.75
        self.MIN_N = 10
        self.R_PLUS = 100

    def update(self, playthrough, max_iterations=1_000):
        # Something like this may allow for better adaptability to new players
        # self.R_PLUS += 5
        # self.MIN_N += 5

        for i in range(max_iterations):
            new_u = self.U.copy()
            delta = 0

            for s in self.S:
                self.N[s] += 1
                if self.N[s] < self.MIN_N:
                    new_u[s] = self.R_PLUS - self.N[s]
                else:
                    new_u[s] = self.R[s] + self.GAMMA * max([self.P[s][next_s] * self.U[next_s] for next_s in self.P[s]])
                
                delta = max(delta, abs(self.U[s] - new_u[s]))

            self.U = new_u
            if delta < self.theta:
                break
