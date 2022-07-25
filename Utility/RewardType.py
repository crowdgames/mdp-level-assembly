from Utility.CustomNode import CustomNode
from enum import Enum

class RewardType(Enum):
    DESIGNER = 0
    PLAYER = 1
    BOTH = 2

def reward_type_to_str(r_type: RewardType) -> str:
    if r_type == RewardType.DESIGNER:
        return 'DESIGNER'
    elif r_type == RewardType.PLAYER:
        return 'PLAYER'
    elif r_type == RewardType.BOTH:
        return 'BOTH'

    raise ValueError(f'Unhandled reward type: {r_type} :: {type(r_type)}')

def set_reward(r_type: RewardType, node: CustomNode):
    if r_type == RewardType.PLAYER:
        node.reward = node.player_reward / node.visited_count
    elif r_type == RewardType.DESIGNER:
        node.reward = node.designer_reward / node.visited_count
    elif r_type == RewardType.BOTH:
        node.reward = (node.player_reward + node.designer_reward) / node.visited_count
    else:
        raise ValueError(f'Unhandled reward type: {r_type}')