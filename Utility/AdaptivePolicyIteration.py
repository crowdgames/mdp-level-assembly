from typing import Dict
from GDM.ADP import policy_iteration
from GDM.Graph import Graph
from Utility import Keys

class AdaptivePolicyIteration:
    def __init__(self, gamma: float, k: int):
        self.k = k
        self.gamma = gamma
        self.current_count = 0

    def get_policy(self, G: Graph, player_won: bool) -> Dict[str, str]:
        if player_won:
            self.current_count = 0
        else:
            self.current_count += 1

        for _ in range(self.current_count):
            neighbors = G.get_node(Keys.START).neighbors
            if len(neighbors) == 1:
                continue

            best_neighbor: str = ""
            best_bc: float = -1
            for tgt in neighbors:
                bc = sum(G.get_node(tgt).behavioral_characteristics)
                if bc > best_bc:
                    best_neighbor = tgt
                    best_bc = bc

            G.remove_edge(Keys.START, best_neighbor)

        return policy_iteration(G, self.gamma, modified=True, in_place=True, policy_k=self.k)
