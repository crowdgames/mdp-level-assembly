from Directors.Keys import *
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

def set_reward(r_type, graph, node_name):
    node = graph.nodes[node_name]
    node[DR] = node[OR] / node[C]
    node[TR] = node[DR] + node[PR]

    if r_type == RewardType.DESIGNER or r_type == RewardType.BOTH:
        r = node[DR]

    if r_type == RewardType.PLAYER or r_type == RewardType.BOTH:
        r = node[PR]
    
    if r_type == RewardType.BOTH:
        r = node[TR]
    
    node[R] = r / node[PC]