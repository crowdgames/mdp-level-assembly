from dataclasses import dataclass
from .PlayerKeys import *

@dataclass
class PlaythroughEntry:
    node_name: str
    percent_completable: float
    player_reward: float
    designer_reward: float
    total_reward: float 
    reward:float

    def to_dict(self):
        return {
            NAME: self.node_name,
            R: self.reward,
            PC: self.percent_completable,
            AR: self.player_reward,
            DR: self.designer_reward,
            TR: self.total_reward
        }
