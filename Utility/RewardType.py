from enum import Enum

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

def get_reward(r_type, segment_entry):
    if r_type == RewardType.DESIGNER:
        return segment_entry.designer_reward
    elif r_type == RewardType.PLAYER:
        return segment_entry.player_reward
    elif r_type == RewardType.BOTH:
        return segment_entry.total_reward

    raise ValueError(f'Unhandled reward type: {r_type} :: {type(r_type)}')