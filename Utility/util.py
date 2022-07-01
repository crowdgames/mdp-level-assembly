import random, sys
import networkx as nx

from json import load as load_file
from random import uniform
from os.path import join
from os import listdir

from Directors.Keys import *
from .NGram import NGram

DEFAULT_PERCENT_COMPLETABLE = 1
DEFAULT_PLAYER_REWARD = 0
DEFAULT_COUNT = 1


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

def __largest_connected_subgraph(graph):
    biggest_comp = None
    for comp in nx.strongly_connected_components(graph):
        if biggest_comp == None or len(comp) > len(biggest_comp):
            biggest_comp = comp

    return graph.subgraph(biggest_comp).copy()

def get_n_gram_graph(config):
    gram = NGram(config.GRAMMAR_SIZE)

    for filename in listdir(config.TRAINING_LEVELS_DIR):
        filepath = join(config.TRAINING_LEVELS_DIR, filename)
        gram.add_sequence(config.read_file(filepath))

    graph = nx.DiGraph()

    for prior in gram.grammar:
        key = str(prior)
        graph.add_node(key)
        graph.nodes[key][P] = prior
        graph.nodes[key][S] = [prior[-1]] 
        graph.nodes[key][R] = 1 # this is set by an agent
        graph.nodes[key][DR] = 1 # this is set by an agent

    for prior in gram.grammar:
        prior_key = str(prior)
        for neighbor in gram.grammar[prior].keys():
            n_prior = prior[1:] + (neighbor,)
            graph.add_edge(prior_key, str(n_prior))

    config.START_NODE = str(list(gram.grammar.keys())[0])

    # we want the graph to be fully connected
    return __largest_connected_subgraph(graph), gram

def __convert_str(string, div):
    return float(string) / div
    # return float(string) * 0.1

def get_level_segment_graph(config, allow_empty_link):
    # get json file that represents the graph
    filename = join(config.BASE_DIR, f'links_{allow_empty_link}.json')
    print(f'Loading links from: {filename}') 
    with open(filename, 'r') as f:
        data = load_file(f)

    # find max behavioral characteristic values. Note: there is kind of a cheat
    # here since I know that only two behavioral characteristics are used for
    # each game.
    dist = 1000
    max_bc = [0,0]
    for key in data.keys():
        a, b, c = key.split(',')
        a = int(a)
        b = int(b)
        c = int(c)

        max_bc[0] = max(max_bc[0], a)
        max_bc[1] = max(max_bc[1], b)

        new_dist = a + b + c
        if new_dist < dist:
            dist = new_dist
            config.START_NODE = key

    config.MAX_BC = max_bc
    
    # build graph from json file
    graph = nx.DiGraph()
    links = []
    for node, next_data in data.items():
        # reward range is [-1,1]
        a, b, _ = node.split(',')
        a = __convert_str(a, max_bc[0])
        b = __convert_str(b, max_bc[1])
        r = (a + b) / 2.0
        # assert r <= 1

        node_filename = f'{join(config.BASE_DIR, "levels", node.replace(",", "_"))}.txt'
        with open(node_filename, 'rt') as infile:
            lines = [l.strip() for l in infile.readlines()]

        slices = tuple(rows_to_slices(lines, config.TRANSPOSE))

        # level segments do not have have a designer preference in terms of probability
        # selection. Multiplication by 1 results in no change.
        graph.add_node(node)
        graph.nodes[node][S] = slices
        graph.nodes[node][OR] = r
        graph.nodes[node][DR] = r
        # graph.nodes[node][R] = r + 1
        graph.nodes[node][C] = 1
        graph.nodes[node][R] = r
        graph.nodes[node][BC] = [a,b]
        graph.nodes[node][PC] = DEFAULT_PERCENT_COMPLETABLE
        graph.nodes[node][PR] = DEFAULT_PLAYER_REWARD

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
                links.append(edge_node)

                graph.add_node(edge_node)
                graph.nodes[edge_node][S] = slices
                graph.nodes[edge_node][C] = DEFAULT_COUNT
                graph.nodes[edge_node][PR] = DEFAULT_PLAYER_REWARD
                graph.nodes[edge_node][PC] = DEFAULT_PERCENT_COMPLETABLE
                # the rest are updated blow

                graph.add_edge(node, edge_node)
                graph.add_edge(edge_node, next_node)

    # edges are the mean reward of the two nodes that they connect
    for e in links:
        src, tgt = e.split('__')
        src_a, src_b, _ =  src.split(',')
        src_a = __convert_str(src_a, max_bc[0])
        src_b = __convert_str(src_b, max_bc[1])

        tgt_a, tgt_b, _ =  tgt.split(',')
        tgt_a = __convert_str(tgt_a, max_bc[0])
        tgt_b = __convert_str(tgt_b, max_bc[1])

        mean_a = (src_a + tgt_a)/2.0
        mean_b = (src_b + tgt_b)/2.0

        graph.nodes[e][OR] = r
        # graph.nodes[e][R] = r + 1
        graph.nodes[e][R] = r
        graph.nodes[e][DR] = (mean_a + mean_b)/2.0
        graph.nodes[e][BC] = [mean_a, mean_b]

    # we want the graph to be fully connected
    return __largest_connected_subgraph(graph)
