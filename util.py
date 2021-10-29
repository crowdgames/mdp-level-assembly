import random, sys
import networkx as nx



def rows_to_slices(rows, transpose):
    if transpose:
        return list(reversed(rows))
    else:
        return [''.join(_)[::-1] for _ in [*zip(*rows)]]

def slices_to_rows(slices, transpose):
    if transpose:
        return list(reversed(slices))
    else:
        return [''.join(_) for _ in [*zip(*slices)]][::-1]

def largest_scc(graph):
    biggest_comp = None
    for comp in nx.strongly_connected_components(graph):
        #sys.stderr.write('component: %d\n' % len(comp))
        if biggest_comp == None or len(comp) > len(biggest_comp):
            biggest_comp = comp
    return graph.subgraph(biggest_comp).copy()

def select_random_next(graph, out_edges):
    nexts = []
    wts = []
    for out_edge in out_edges:
        nexts.append((out_edge[1]))
        if 'weight' in graph.edges[out_edge]:
            wts.append(graph.edges[out_edge]['weight'])
        else:
            wts.append(1)

    return random.choices(nexts, weights=wts, k=1)[0]

def print_level(level, path=None, goals=None):
    path_start = None
    path_end = None
    path_set = set()
    if path != None:
        path_start = (path[0][0], path[0][1])
        path_end = (path[-1][0], path[-1][1])
        for node in path:
            path_set.add((node[0], node[1]))

    goal_set = goals if goals != None else set()

    for ir, row in enumerate(level):
        for ic, t in enumerate(row):
            pt = (ic, ir)
            if pt == path_start:
                sys.stdout.write('@')
            elif pt == path_end:
                sys.stdout.write('*')
            elif pt in path_set:
                sys.stdout.write('.')
            elif pt in goal_set:
                sys.stdout.write('!')
            else:
                sys.stdout.write(t)
        sys.stdout.write('\n')
