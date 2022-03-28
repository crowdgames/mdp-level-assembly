from tkinter import SOLID
from Utility.SummervilleAgent import find_path
from os.path import join

WRAPS = True
TRANSPOSE = True
START_NODE = '0,2,0'
PADDING_SIZE = 2
NAME = 'icarus'
MAX_BC = None
NUM_BC = 2
REWARD_TYPE = None
ALLOW_EMPTY_LINK = True
GRAMMAR_SIZE = 2
GRAM = None

SOLIDS = set()
SOLIDS.add('#')
SOLIDS.add('T')
SOLIDS.add('X')
SOLIDS.add('D')
SOLIDS.add('d')
SOLIDS.add('H')

DOOR = 'D'
MOVING = 'M'
HAZARD = 'H'

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

BASE_DIR = join('.', 'GramElitesData', 'IcarusData', 'gram_elites')
TRAINING_LEVELS_DIR = 'IcarusLevels'
S = '0_0_0'

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
