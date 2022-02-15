from Utility.Math import get_slope_and_intercept
from os.path import join

WRAPS = False
TRANSPOSE = False
START = (1,1,-1)

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

def linearity_with_heights(heights):
    '''
    a gap is not supposed to be included in the linearity calculation. The input
    for least squares is offset to accommodate this.
    '''
    x = []
    y = []

    subtract_by = 0
    for i in range(len(heights)):
        h = heights[i]

        if h != -1:
            x.append(i - subtract_by)
            y.append(h)
        else:
            subtract_by += 1

    slope, expected = get_slope_and_intercept(x, y)
    score = 0

    for height in y:
        if height != -1:
            score += abs(expected - height)
            expected += slope

    return score

def min_height(column):
    '''
    -1 means that there is no solid found.
    '''
    found = False
    height = 0
    while height <= len(column) - 1:
        if column[height] in SOLIDS:
            found = True
        elif found:
            break

        height += 1
    
    return height - 1 if found else -1

def linearity(level):
    return linearity_with_heights([min_height(col) for col in level])

def contains_enemy(column):
    found_enemy = False
    for token in column:
        if token in ENEMIES:
            found_enemy = True
            break

    return found_enemy

def contains_gap(column):
    return column[0] not in SOLIDS

def leniency(level):
    score = 0

    for column in level:
        if contains_enemy(column):
            score += 0.5
        
        if contains_gap(column):
            score += 0.5

    return score 

def get_reward(slices):
    # TODO: optimize to use one for loop
    return linearity(slices) + leniency(slices)