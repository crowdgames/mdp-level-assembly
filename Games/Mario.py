WRAPS = False

def find_goals(level, start_pos, index, solids):
    goals = set()
    for ic in range(index, 2, -1):
        if ic <= start_pos[0] + 1:
            return None
        
        found_solid = False
        for ir in range(len(level) - 1, -1, -1):
            if level[ir][ic] in solids:
                found_solid = True
            else:
                if found_solid:
                    goals.add((ic, ir))
        if len(goals) != 0:
            return goals
    return None

def find_start(lvl, sz, solids):
    return (0, 0, -1)

def reward(px, py, x, y, j, ji):
    if False:
        if ji == 0 or ji == 1:
            return 1
    elif False:
        if y >= 11:
            return 1
    elif False:
        if ji == -1:
            return 1
    elif True:
        if 5 <= y and y <= 7:
            return 1
    else:
        if y <= 3:
            return 1
    return None

