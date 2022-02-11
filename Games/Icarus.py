WRAPS = True


def find_start(level, index, solids):
    for ir in range(len(level) - 2, len(level) - index, -1):
        for ic in range(len(level[0])):
            if not level[ir][ic] in solids and level[ir + 1][ic] in solids:
                return (ic, ir, -1)
    return None

def find_goals(level, start_pos, index, solids):
    goals = set()
    for ir in range(len(level) - 1 - index, len(level) - 1):
        if ir >= start_pos[1] - 1:
            return None
        
        for ic in range(len(level[0])):
            if not level[ir][ic] in solids:
                goals.add((ic, ir))
        if len(goals) != 0:
            return goals
    return None

def reward(px, py, x, y, j, ji):
    if False:
        if 4 <= x and x <= 12:
            return 1
        if abs(x - px) > 2:
            return -5
    elif False:
        if 4 <= x and x <= 12:
            return None
        if abs(x - px) > 2:
            return 5
    else:
        if abs(x - px) > 2:
            return 1
    return None
