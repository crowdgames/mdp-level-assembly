import random, sys
import networkx as nx

from json import load as load_file
from os.path import join


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

def get_graph(BASE_DIR, transpose, link_name='links.json'):
    # get json file that represents the graph
    with open(join(BASE_DIR, link_name), 'r') as f:
        data = load_file(f)

    # find max behavioral characteristic values. Note: there is kind of a cheat
    # here since I know that only two behavioral characteristics are used for
    # each game.
    max_bc = [0.0,0.0]
    for key in data.keys():
        a, b, _ = key.split(',')
        max_bc[0] = max(max_bc[0], float(a))
        max_bc[1] = max(max_bc[1], float(b))

    # build graph from json file
    graph = nx.DiGraph()
    for node, next_data in data.items():
        a, b, _ = key.split(',')
        r = (float(a) / max_bc[0]) + (float(b) / max_bc[1])

        node_filename = f'{join(BASE_DIR, "levels", node.replace(",", "_"))}.txt'
        with open(node_filename, 'rt') as infile:
            lines = [_.strip() for _ in infile.readlines()]

        slices = tuple(rows_to_slices(lines, transpose))
        # graph.add_node(node, slices=slices, r=1, max_r=get_reward(slices))
        graph.add_node(node, slices=slices, r=r, max_r=r)

        for next_node, edge_data in next_data.items():
            edge_data_use = edge_data['tree search']
            
            if edge_data_use['percent_playable'] != 1.0:
                continue
            
            assert (node, next_node) not in graph.edges

            # If the link is not empty than we create a node for that link. If it
            # is empty, then no node is created and we create an edge directly
            # between the two nodes.
            edge_slices = tuple(edge_data_use['link'])
            if len(edge_slices) == 0:
                graph.add_edge(node, next_node)
            else:
                edge_node = f'{node}__{next_node}'

                # graph.add_node(edge_node, slices=edge_slices, r=1, max_r=r)
                graph.add_node(edge_node, slices=edge_slices, r=r, max_r=r)
                graph.add_edge(node, edge_node)
                graph.add_edge(edge_node, next_node)

    # get largest strongly connected version of the graph to remove deadends
    biggest_comp = None
    for comp in nx.strongly_connected_components(graph):
        if biggest_comp == None or len(comp) > len(biggest_comp):
            biggest_comp = comp

    return graph.subgraph(biggest_comp).copy()