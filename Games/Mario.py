from sre_constants import JUMP
from typing import Set, List, Tuple 

from Utility.SummervilleAgent import find_path
from Utility import RewardType, slices_to_rows, rows_to_slices
from os.path import join

from .Config import Config

# view smb.json in TheVGLC
SOLIDS: Set[str] = set()
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
JUMPS: List[List[Tuple[int, int]]] = [
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

def read_file(filepath: str) -> List[str]:
    with open(filepath) as f:
        lines = [l.strip() for l in f.readlines()]

    return rows_to_slices(lines, False)

def get_furthest_xy(config: Config, lvl: List[str]) -> Tuple[int, int]:
    lvl.insert(0, 'X-------------')
    lvl.insert(0, 'X-------------')
    lvl.append('X-------------')
    lvl.append('X-------------')
    formatted_lvl = slices_to_rows(lvl, False)

    START = (0, len(formatted_lvl)-2, -1)
    heuristic = lambda pos: (len(lvl) - 1 - pos[0])**2

    x, y = find_path(formatted_lvl, START, config.JUMPS, config.SOLIDS, config.WRAPS, heuristic)
    
    lvl.pop(0)
    lvl.pop(0)
    lvl.pop()
    lvl.pop()

    return x, y

def player_reward(slice: List[str]) -> float:
    total = 0
    for char in slice:
        if char in SOLIDS:
            total += 1
            continue

    return total/len(slice)

def designer_reward(slice: List[str]) -> float:
    return 'E' in slice

def level_to_str(columns: List[str]) -> str:
    return '\n'.join(slices_to_rows(columns, False))

MARIO = Config(
    WRAPS=False,
    TRANSPOSE=False,
    START_NODE = '0,0,0',
    PADDING_SIZE = 2,
    NAME = 'mario',
    MAX_BC = -1000000000,
    NUM_BC = 2,
    REWARD_TYPE = RewardType.BOTH,
    ALLOW_EMPTY_LINK = True,
    SOLIDS=SOLIDS,
    JUMPS=JUMPS,
    GRAMMAR_SIZE=3,
    BASE_DIR=join('.', 'GramElitesData', 'MarioData', 'gram_elites'),
    TRAINING_LEVELS_DIR = join('TrainingLevels', 'Mario'),
    read_file=read_file,
    get_furthest_xy=get_furthest_xy,
    player_reward=player_reward,
    level_to_str=level_to_str,
    designer_reward=designer_reward
)







