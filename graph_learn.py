import argparse, math, pickle, pprint, random, sys
import networkx as nx
import SummervilleAgent, util



ALPHA   = 0.10
LAMBDA  = 0.90
EPSILON = 0.10



def count_tile(slices, tile):
    tile_count = 0
    for slc in slices:
        tile_count += slc.count(tile)
    return tile_count
    
def count_tile_level(graph, nodes, tile):
    count = 0
    for node in nodes:
        count += count_tile(graph.nodes[node]['slices'], tile)
    return count

def nodes_to_slices(graph, nodes, prev_node=None):
    slices_out = []
    edges_out = []
    
    for ni, node in enumerate(nodes):
        node_slices = graph.nodes[node]['slices']
        incoming_edge = (prev_node, node)
        
        slices_out += node_slices
        edges_out += ([incoming_edge] * len(node_slices))
        prev_node = node

    return slices_out, edges_out

def slices_to_level(graph, slices):
    return util.slices_to_rows(slices, graph.graph['transpose'])

def nodes_to_level(graph, nodes):
    slices_out, edges_out = nodes_to_slices(graph, nodes)
    return slices_to_level(graph, slices_out), edges_out



def q_table_init(graph):
    q = {}

    for edge in graph.edges:
        q[edge] = 0.0

    return q
    
def q_table_update(graph, q, edge, value):
    max_next_q = -1e100
    out_edges = list(graph.out_edges(edge[1]))
    for out_edge in out_edges:
        max_next_q = max(max_next_q, q[out_edge])

    q[edge] = (1.0 - ALPHA) * q[edge] + ALPHA * (value + LAMBDA * max_next_q)

def q_table_next(graph, q, node, eps):
    out_edges = list(graph.out_edges(node))

    if False:
        nexts = []
        wts = []
        for out_edge in out_edges:
            nexts.append(out_edge[1])
            wts.append(math.exp(q[out_edge]))
        return random.choices(nexts, weights=wts, k=1)[0]

    else:
        # selecting edge with max q seems to work much better

        if random.random() < eps:
            nexts = []
            for out_edge in out_edges:
                nexts.append(out_edge[1])
            return random.sample(nexts, k=1)[0]

        else:
            best_q = -1e100
            next_nodes = []

            for out_edge in out_edges:
                out_q = q[out_edge]
                if out_q > best_q:
                    best_q = out_q
                    next_nodes = [out_edge[1]]
                elif out_q == best_q:
                    next_nodes.append(out_edge[1])

            return random.sample(next_nodes, 1)[0]

    

def gen_level_random(graph, size, start=None):
    curr_node = start if start != None else random.sample(graph.nodes, 1)[0]
    nodes = [curr_node]
    nslices = len(graph.nodes[curr_node]['slices'])

    while nslices < size:
        out_edges = list(graph.out_edges(curr_node))

        next_node = util.select_random_next(graph, out_edges)

        curr_node = next_node
        nodes.append(curr_node)
        nslices += len(graph.nodes[curr_node]['slices'])

    return nodes

def gen_level_greedy(graph, size, tile, start=None):
    curr_node = start if start != None else random.sample(graph.nodes, 1)[0]
    nodes = [curr_node]
    nslices = len(graph.nodes[curr_node]['slices'])

    while nslices < size:
        out_edges = list(graph.out_edges(curr_node))

        best_nexts = []
        best_count = 0
        
        for out_edge in out_edges:
            out_slices = graph.nodes[out_edge[1]]['slices']
            tile_count = count_tile(out_slices, tile)

            if tile_count > best_count:
                best_count = tile_count
                best_nexts = [out_edge[1]]
            elif tile_count == best_count:
                best_nexts.append(out_edge[1])

        if len(best_nexts) > 0:
            next_node = random.sample(best_nexts, 1)[0]
        
        else:
            next_node = util.select_random_next(graph, out_edges)

        curr_node = next_node
        nodes.append(curr_node)
        nslices += len(graph.nodes[curr_node]['slices'])

    return nodes

def learn_q_edge_shuffle(graph, tile):
    q = q_table_init(graph)

    for ii in range(1000):
        edges = list(graph.edges)
        random.shuffle(edges)

        for edge in edges:
            out_slices = graph.nodes[edge[1]]['slices']
            value = count_tile(out_slices, tile)

            q_table_update(graph, q, edge, value)

    return q

def learn_q_level(graph, size, tile):
    q = q_table_init(graph)

    iters = 10 * len(q)

    for ii in range(iters):
        nodes = gen_level_random(graph, size)
        level, level_edges = nodes_to_level(graph, nodes)

        if False:
            for ir, row in enumerate(level):
                for ic, t in enumerate(row):
                    if graph.graph['transpose']:
                        edge = level_edges[-ir - 1]
                    else:
                        edge = level_edges[ic]

                    if edge[0] == None:
                        continue

                    if t == TILE:
                        value = 1
                    else:
                        value = 0

                    q_table_update(graph, q, edge, value)

        else:
            edge_reward = {}

            for edge in level_edges:
                if edge[0] == None:
                    continue

                edge_reward[edge] = 0
        
            if graph.graph['transpose']:
                for ir in range(len(level) - 1, -1, -1):
                    edge = level_edges[-ir - 1]
                    if edge[0] == None:
                        continue

                    for ic in range(len(level[0])):
                        if level[ir][ic] == TILE:
                            edge_reward[edge] += 1
            else:
                for ic in range(len(level[0])):
                    edge = level_edges[ic]
                    if edge[0] == None:
                        continue

                    for ir in range(len(level)):
                        if level[ir][ic] == TILE:
                            edge_reward[edge] += 1

            for edge in level_edges:
                if edge[0] == None:
                    continue

                value = edge_reward[edge]

                q_table_update(graph, q, edge, value)

    return q

def gen_level_q(graph, q, eps, size, start=None):
    curr_node = start if start != None else random.sample(graph.nodes, 1)[0]
    nodes = [curr_node]
    nslices = len(graph.nodes[curr_node]['slices'])

    while nslices < size:
        curr_node = q_table_next(graph, q, curr_node, eps)

        nodes.append(curr_node)
        nslices += len(graph.nodes[curr_node]['slices'])

    return nodes

def init_q(graph):
    q = q_table_init(graph)

    return q

def update_q(graph, q, level, level_edges, path, reward_func, transpose):
    total_reward = 0
    
    for prev_pnode, pnode in zip(path, path[1:]): # first got counted on previous segment
        px = prev_pnode[0]
        py = prev_pnode[1]
        x = pnode[0]
        y = pnode[1]
        j = pnode[2]
        ji = -1 if (j == -1) else pnode[3]

        if transpose:
            edge = level_edges[-y-1]
        else:
            edge = level_edges[x]

        if edge[0] == None:
            continue

        value = reward_func(px, py, x, y, j, ji)
        
        if value == None:
            value = 0.0
            #continue

        total_reward += value

        q_table_update(graph, q, edge, value)

    return total_reward

def update_q_batch(graph, q, level, level_edges, path, reward_func, transpose):
    total_reward = 0

    # TODO: should probably account for edges that were not reached by path rather than giving 0 reward!
    
    edge_reward = {}
    for edge in level_edges:
        if edge[0] == None:
            continue

        edge_reward[edge] = 0

    for prev_pnode, pnode in zip(path, path[1:]): # first got counted on previous segment
        px = prev_pnode[0]
        py = prev_pnode[1]
        x = pnode[0]
        y = pnode[1]
        j = pnode[2]
        ji = -1 if (j == -1) else pnode[3]

        if transpose:
            edge = level_edges[-y-1]
        else:
            edge = level_edges[x]

        if edge[0] == None:
            continue

        value = reward_func(px, py, x, y, j, ji)
        
        if value == None:
            continue

        total_reward += value

        edge_reward[edge] += value

    for edge in level_edges:
        if edge[0] == None:
            continue

        value = edge_reward[edge]
        
        q_table_update(graph, q, edge, value)

    return total_reward

def find_goals_mario(level, start_pos, index, solids):
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

def rewards_mario(px, py, x, y, j, ji):
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

def find_start_icarus(level, index, solids):
    for ir in range(len(level) - 2, len(level) - index, -1):
        for ic in range(len(level[0])):
            if not level[ir][ic] in solids and level[ir + 1][ic] in solids:
                return (ic, ir, -1)
    return None

def find_goals_icarus(level, start_pos, index, solids):
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

def rewards_icarus(px, py, x, y, j, ji):
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



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate levels.')
    parser.add_argument('filename', type=str, help='Graph files.')
    parser.add_argument('--blocksize', type=int, required=True, help='Generate with blocks of given size.', default=None)
    run_group = parser.add_mutually_exclusive_group(required=True)
    run_group.add_argument('--rungen', action='store_true', help='Run continuous generation.')
    run_group.add_argument('--comparetile', type=str, help='Compare apporaches using given tile.', default=None)
    game_group = parser.add_mutually_exclusive_group(required=True)
    game_group.add_argument('--mario', action='store_true', help='Use Mario.')
    game_group.add_argument('--icarus', action='store_true', help='Use Icarus.')
    args = parser.parse_args()

    with open(args.filename, 'rb') as f:
        graph = pickle.load(f)

    if args.icarus:
        if not graph.graph['transpose']:
            raise RuntimeError('Icarus must use transposed slices')
        GAME_jumps = SummervilleAgent.JUMPS
        GAME_solids = SummervilleAgent.SOLIDS_ICARUS
        GAME_wrapx = True
        GAME_start_pos = find_start_icarus
        GAME_find_goals = find_goals_icarus
        GAME_rewards = rewards_icarus
    else:
        if graph.graph['transpose']:
            raise RuntimeError('Mario must not use transposed slices')
        GAME_jumps = SummervilleAgent.JUMPS
        GAME_solids = SummervilleAgent.SOLIDS_MARIO
        GAME_wrapx = False
        GAME_start_pos = lambda lv, sz, solids: (0, 0, -1)
        GAME_find_goals = find_goals_mario
        GAME_rewards = rewards_mario

    # TODO: get farthest point agent could find so reward can incorporate playability?
    
    if args.rungen:
        block_size = args.blocksize

        REW_AVG = 10

        q = init_q(graph)
        running_reward = []

        while True:
            #nodes = gen_level_random(graph, block_size * 3, None)
            nodes = gen_level_q(graph, q, EPSILON, block_size * 3, None)
            level_slices, level_edges = nodes_to_slices(graph, nodes, None)
            
            level = slices_to_level(graph, level_slices)

            start_pos = GAME_start_pos(level, block_size, GAME_solids)
            if start_pos == None:
                print('*** RESTARTING: no start pos ***')
                continue

            play_goals = GAME_find_goals(level, start_pos, block_size * 2 - 1, GAME_solids) # TODO: make sure in check_path or allow any?
            if play_goals == None:
                print('*** RESTARTING: no initial play goals ***')
                continue
                
            play_path = SummervilleAgent.find_path(level, start_pos, play_goals, GAME_jumps, GAME_solids, GAME_wrapx)
            if play_path == None:
                print('*** RESTARTING: no initial play path ***')
                continue

            reward = update_q_batch(graph, q, level, level_edges, play_path, GAME_rewards, graph.graph['transpose'])
            running_reward = (running_reward + [reward])[-REW_AVG:]
            util.print_level(level, play_path, play_goals)
            print('reward:', reward)
            print('avg total reward:', sum(running_reward) / len(running_reward))
            print()

            while True:
                if graph.graph['transpose']:
                    end_y = play_path[-1][1]
                    remove_slices = (len(level) - 1) - end_y - block_size + 1
                    # TODO: check end_y ~>~ block_size ?
                else:
                    end_x = play_path[-1][0]
                    remove_slices = end_x - block_size + 1
                    # TODO: check end_x > block_size ?
        
                orig_slices = level_slices[remove_slices:]
                orig_edges = level_edges[remove_slices:]

                gen_len = (block_size * 3) - len(orig_slices)

                prev_node = nodes[-1]
                #nodes = gen_level_random(graph, gen_len, orig_nodes[-1])[1:]
                nodes = gen_level_q(graph, q, EPSILON, gen_len + len(graph.nodes[prev_node]['slices']), prev_node)[1:]
                new_slices, new_edges = nodes_to_slices(graph, nodes, prev_node)

                if graph.graph['transpose']:
                    start_pos = play_path[-1][0:1] + (end_y + len(new_slices),) + play_path[-1][2:]
                else:
                    start_pos = (end_x - remove_slices,) + play_path[-1][1:]

                level_slices = orig_slices + new_slices
                level_edges = orig_edges + new_edges

                level = slices_to_level(graph, level_slices)

                play_goals = GAME_find_goals(level, start_pos, block_size * 2 - 1, GAME_solids) # TODO: make sure in check_path or allow any?
                if play_goals == None:
                    print('*** RESTARTING: no continued play goals ***')
                    continue

                play_path = SummervilleAgent.find_path(level, start_pos, play_goals, GAME_jumps, GAME_solids, GAME_wrapx)
                if play_path == None:
                    print('*** RESTARTING: no continued play path ***')
                    break

                reward = update_q_batch(graph, q, level, level_edges, play_path, GAME_rewards, graph.graph['transpose'])
                running_reward = (running_reward + [reward])[-REW_AVG:]
                util.print_level(level, play_path, play_goals)
                print('reward:', reward)
                print('avg total reward:', sum(running_reward) / len(running_reward))
                print()
                #sys.exit(-1)

    elif args.comparetile != None:
        LOOP = 10000
        TILE = args.comparetile

        #q = learn_q_edge_shuffle(graph, TILE)
        q = learn_q_level(graph, args.blocksize, TILE)

        # TODO: account for different level lengths, i.e. normalize by total tiles generated ?

        APPROACHES = {
            'random': lambda: gen_level_random(graph, args.blocksize),
            'greedy': lambda: gen_level_greedy(graph, args.blocksize, TILE),
            'q':      lambda: gen_level_q(graph, q, 0.0, args.blocksize)
            }

        # TODO: maybe start all approaches from the same random node?
        cts = {}
        for name, gen_fn in APPROACHES.items():
            cts[name] = []
            
            for ii in range(LOOP):
                nodes = gen_fn()
                level, edges = nodes_to_level(graph, nodes)
                count = count_tile_level(graph, nodes, TILE)
                cts[name].append((count, level))

            cts[name] = sorted(cts[name])
        
        import statistics
        print('FILE:', args.filename, 'TILE:', TILE, 'SIZE:', args.blocksize)
        print('%7s %6s %6s %6s %6s' % ('', 'min', 'mean', 'med', 'max'))
        for name in APPROACHES.keys():
            lst = [_[0] for _ in cts[name]]
            print('%6s: %6.2f %6.2f %6.2f %6.2f' % (name, min(lst), statistics.mean(lst), statistics.median(lst), max(lst)))

        print()
        print('greedy med:')
        util.print_level(cts['greedy'][LOOP // 2][1])
        
        print()
        print('greedy max:')
        util.print_level(cts['greedy'][-1][1])
        
        print()
        print('q med:')
        util.print_level(cts['q'][LOOP // 2][1])

        print()
        print('q max:')
        util.print_level(cts['q'][-1][1])
