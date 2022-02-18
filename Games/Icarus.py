from Utility.SummervilleAgent import find_path
from os.path import join

WRAPS = True
TRANSPOSE = True
START_NODE = '0,2,0'
PADDING_SIZE = 2
NAME = 'icarus'


SOLIDS = set()
SOLIDS.add('#')
SOLIDS.add('T')
SOLIDS.add('X')
SOLIDS.add('D')
SOLIDS.add('d')

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
S = '0_0_0'


def get_furthest_xy(lvl):
    play_slices = list(lvl)

    # add an area for the player to start at the bottom
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

    return x / len(lvl), y /len(lvl[0])
