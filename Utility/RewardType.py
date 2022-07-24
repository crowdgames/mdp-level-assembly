from enum import Enum
from GDM.Graph import Graph

from Utility.CustomNode import CustomNode

class RewardType(Enum):
    DESIGNER = 0
    PLAYER = 1
    BOTH = 2

def reward_type_to_str(r_type):
    if r_type == RewardType.DESIGNER:
        return 'DESIGNER'
    elif r_type == RewardType.PLAYER:
        return 'PLAYER'
    elif r_type == RewardType.BOTH:
        return 'BOTH'

    raise ValueError(f'Unhandled reward type: {r_type} :: {type(r_type)}')

def set_reward(r_type: RewardType, node: CustomNode):
    percent_completable = max(0.01, node.percent_completable) # prevent divide by zero
    if r_type == RewardType.PLAYER:
        node.reward = node.player_reward
    elif r_type == RewardType.DESIGNER:
        node.reward = node.designer_reward / (node.visited_count * percent_completable)
    elif r_type == RewardType.BOTH:
        node.reward = (node.designer_reward/(node.visited_count*percent_completable)) + node.player_reward
    else:
        raise NotImplementedError(f'Unhandled reward type: {r_type}')