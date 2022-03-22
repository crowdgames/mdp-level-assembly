from Utility.SummervilleAgent import find_path
from Utility import slices_to_rows
from os.path import join

WRAPS = False
TRANSPOSE = False
START_NODE = '0,0,0'
PADDING_SIZE = 2
NAME = 'mario'
MAX_BC = None
NUM_BC = 2
REWARD_TYPE = None
ALLOW_EMPTY_LINK = True


# view smb.json in TheVGLC
SOLIDS = set()
SOLIDS.add('X')
SOLIDS.add('S')
SOLIDS.add('?')
SOLIDS.add('Q')
SOLIDS.add('<')
SOLIDS.add('>')
SOLIDS.add('[')
SOLIDS.add(']')
SOLIDS.add('B')
SOLIDS.add('b')

ENEMIES = set()
ENEMIES.add('E')
ENEMIES.add('B')
ENEMIES.add('b')

# modified from past work by seth cooper
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

BASE_DIR = join('.', 'GramElitesData', 'MarioData', 'gram_elites')
S = '0_0_0'

def get_furthest_xy(lvl):
    lvl.insert(0, 'X-------------')
    lvl.insert(0, 'X-------------')
    lvl.append('X-------------')
    lvl.append('X-------------')
    formatted_lvl = slices_to_rows(lvl, False)

    START = (0, len(formatted_lvl)-2, -1)
    heuristic = lambda pos: (len(lvl) - 1 - pos[0])**2

    x, y = find_path(formatted_lvl, START, JUMPS, SOLIDS, WRAPS, heuristic)
    
    lvl.pop(0)
    lvl.pop(0)
    lvl.pop()
    lvl.pop()

    return x, y