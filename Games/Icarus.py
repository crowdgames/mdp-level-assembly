WRAPS = True
TRANSPOSE = True

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

def density(slices):
    num_count_blocks = 0
    total_number_of_blocks = 0
    for sl in slices:
        for bl in sl:
            if bl in SOLIDS:
                num_count_blocks += 1
        total_number_of_blocks += len(sl)

    return num_count_blocks / total_number_of_blocks

def leniency(slices):
    count = 0
    for sl in slices:
        if HAZARD in sl:
            count += 1/3
        if DOOR in sl:
            count += 1/3
        if MOVING in sl:
            count += 1/3

    return count / len(slices)

def get_reward(slices):
    # TODO: optimize to use one for loop
    return density(slices) + leniency(slices)
