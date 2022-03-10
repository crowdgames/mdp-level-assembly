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

def get_reward(r_type, designer_r, player_r):
    if r_type == RewardType.DESIGNER:
        return designer_r
    elif r_type == RewardType.PLAYER:
        return player_r
    elif r_type == RewardType.BOTH:
        return designer_r + player_r

    raise ValueError(f'Unhandled reward type: {r_type} :: {type(r_type)}')