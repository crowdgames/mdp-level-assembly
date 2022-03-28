from .PlayerKeys import *

class PlaythroughEntry:
    def __init__(self, node, percent_completable, player_reward):
        self.node_name = node
        self.percent_completable = percent_completable
        self.player_reward = player_reward
        self.designer_reward = 0  # this is set later in the process
        self.total_reward = 0     # this is set later in the process

    def to_dict(self):
        return {
            NAME: self.node_name,
            PC: self.percent_completable,
            AR: self.player_reward,
            DR: self.designer_reward,
            TR: self.total_reward
        }