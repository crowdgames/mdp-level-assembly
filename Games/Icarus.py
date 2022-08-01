from Games.Config import Config
from Utility import RewardType
from Utility.SummervilleAgent import find_path

from typing import List
from os.path import join

SOLIDS = set()
SOLIDS.add('#')
SOLIDS.add('T')
SOLIDS.add('X')
SOLIDS.add('D')
SOLIDS.add('d')
SOLIDS.add('H')


JUMPS = [
    [
        [0,-1],
        [0,-2],
        [0,-3],
        [1,-3],
        [1,-4]
    ],
    [
        [0,-1],
        [0,-2],
        [0,-3],
        [0,-4],
        [1,-4]
    ],
    [
        [0,-1],
        [1,-1],
        [1,-2],
        [1,-3],
        [1,-4],
        [2,-4]
    ],
    [
        [0,-1],
        [1,-1],
        [1,-2],
        [2,-2],
        [2,-3],
        [3,-3],
        [3,-4],
        [4,-4],
        [5,-4],
        [5,-3],
        [6,-3],
        [7,-3],
        [7,-2],
        [8,-2],
        [8,-1]
    ],
    [
        [0,-1],
        [1,-1],
        [1,-2],
        [2,-2],
        [2,-3],
        [3,-3],
        [3,-4],
        [4,-4],
        [5,-4],
        [6,-4],
        [6,-3],
        [7,-3],
        [7,-2],
        [8,-2],
        [8,-1]
    ]
]

def read_file(filepath):
    with open(filepath) as f:
        lines = [l.strip() for l in reversed(f.readlines())]

    return lines

def get_furthest_xy(lvl):
    play_slices = list(lvl)

    # add an area for the player to start at the bottom
    if play_slices[0] == '################':
        play_slices.insert(1, '----------------')
    else:
        play_slices.insert(0, '----------------')
        play_slices.insert(0, '################')

    # extend the top by copying the blocks
    # should ensure the player can jump up above the top but not by landing on what was therex
    play_slices.append(play_slices[-1])
    play_slices.append(play_slices[-1])

    formatted_lvl = list(reversed(play_slices))
    heuristic = lambda pos: (pos[1])**2
    START = (1, len(play_slices)-2, -1)

    x, y = find_path(formatted_lvl, START, JUMPS, SOLIDS, WRAPS, heuristic)
    
    formatted_lvl.pop(0)
    formatted_lvl.pop(0)
    formatted_lvl.pop()
    formatted_lvl.pop()

    return x / len(lvl[0]), y /len(lvl)

def player_reward(slice):
    total = 0
    for char in slice:
        if char in SOLIDS:
            total += 1
            continue

    return total/len(slice)

def level_to_str(columns: List[str]) -> str:
    raise NotImplementedError('Icarus config does not implement level_to_str.')

ICARUS = Config(
    WRAPS=True,
    TRANSPOSE=True,
    START_NODE = '0,2,0',
    PADDING_SIZE = 2,
    NAME = 'icarus',
    MAX_BC = -1000000000,
    NUM_BC = 2,
    REWARD_TYPE = RewardType.BOTH,
    ALLOW_EMPTY_LINK = True,
    SOLIDS=SOLIDS,
    JUMPS=JUMPS,
    GRAMMAR_SIZE=3,
    BASE_DIR=join('.', 'GramElitesData', 'IcarusData', 'gram_elites'),
    TRAINING_LEVELS_DIR = join('TrainingLevels', 'Icarus'),
    read_file=read_file,
    get_furthest_xy=get_furthest_xy,
    player_reward=player_reward,
    level_to_str=level_to_str,
    designer_reward=None
)