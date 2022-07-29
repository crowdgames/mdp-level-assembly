from typing import List, Tuple

from json import load as load_file
from GDM.Graph import Graph
from os.path import join
from os import listdir
import sys
from Games import Config
from Utility import Keys
from Utility.NGramNode import NGramNode
from Utility.CustomEdge import CustomEdge

from Utility.Keys import DEATH, START

from .CustomNode import CustomNode
from .NGram import NGram

DEFAULT_PERCENT_COMPLETABLE = 1
DEFAULT_PLAYER_REWARD = 0
DEFAULT_COUNT = 1
FAIL_PROB = 0.01


def rows_to_slices(rows: List[str], transpose: bool) -> List[str]:
    if transpose:
        return list(reversed(rows))
    else:
        return [''.join(_)[::-1] for _ in [*zip(*rows)]]

def slices_to_rows(slices: List[str], transpose: bool) -> List[str]:
    if transpose:
        return list(reversed(slices))
    else:
        return [''.join(_) for _ in [*zip(*slices)]][::-1]

def clean_graph(G: Graph):
    node_removed = True
    while node_removed:
        node_removed = False
        remove = []
        for node in G.nodes.values():
            if len(node.neighbors) == 0 and not node.is_terminal:
                remove.append(node.name)

        for node in remove:
            G.remove_node(node)
            node_removed = True


def print_level(level: List[str], path=None, goals=None):
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

def get_n_gram_graph(config: Config) -> Tuple[Graph, NGram]:
    gram = NGram(config.GRAMMAR_SIZE)

    for filename in listdir(config.TRAINING_LEVELS_DIR):
        filepath = join(config.TRAINING_LEVELS_DIR, filename)
        gram.add_sequence(config.read_file(filepath))

    G = Graph()
    G.add_default_node(START, reward=0)
    G.add_default_node(DEATH, reward=-1, terminal=True) # was 0?
    
    for prior in gram.grammar:
        key = str(prior)
        G.add_node(NGramNode(key, 1, 0, False, set(), 1, 1, 0, [prior[-1]], (), prior, 1))

    for prior in gram.grammar:
        prior_key = str(prior)
        for neighbor in gram.grammar[prior].keys():
            n_prior = prior[1:] + (neighbor,)
            G.add_edge(CustomEdge(prior_key, str(n_prior), [(str(n_prior), 1-FAIL_PROB), (DEATH, FAIL_PROB)]))

    first_neighbor = str(list(gram.grammar.keys())[0])
    config.START_NODE = first_neighbor
    G.add_edge(CustomEdge(Keys.START, first_neighbor, [(first_neighbor, 1-FAIL_PROB), (DEATH, FAIL_PROB)]))
    
    
    clean_graph(G)
    return G, gram

def __convert_str(string: str, div: float) -> float:
    return float(string) / div
    # return float(string) * 0.1

def get_level_segment_graph(config, allow_empty_link: bool):
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
    links = []
    G = Graph()
    G.add_default_node(START, reward=0)
    G.add_default_node(DEATH, reward=-1, terminal=True) # was 0?
    
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
        if node in G.nodes:
            temp_node = G.get_node(node)
            temp_node.reward = r
            temp_node.designer_reward = r
            temp_node.slices = slices
            temp_node.behavioral_characteristics = (a,b)
        else:
            G.add_node(CustomNode(node, r, 0, False, set(), r, 0, 0, slices, (a,b)))

        for next_node, edge_data in next_data.items():
            edge_data_use = edge_data['tree search']
            
            if edge_data_use['percent_playable'] != 1.0:
                continue
            
            assert (node, next_node) not in G.edges

            if next_node not in G.nodes:
                G.add_node(CustomNode(next_node, 0, 0, False, set(), 0, 0, 0, (), ()))

            # If the link is not empty than we create a node for that link. If it
            # is empty, then no node is created and we create an edge directly
            # between the two nodes.
            edge_slices = tuple(edge_data_use['link'])
            if len(edge_slices) == 0:
                G.add_edge(CustomEdge(node, next_node, [(next_node, 1-FAIL_PROB), (DEATH, FAIL_PROB)]))
            else:
                edge_node = f'{node}__{next_node}'
                links.append(edge_node)

                G.add_node(CustomNode(edge_node, 0, 0, False, set(), 0, 0, 0, slices, (-1, -1)))
                G.add_edge(CustomEdge(node, edge_node, [(edge_node, 1-FAIL_PROB), (DEATH, FAIL_PROB)]))
                G.add_edge(CustomEdge(edge_node, next_node, [(next_node, 1-FAIL_PROB), (DEATH, FAIL_PROB)]))

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

        node = G.get_node(e)
        node.reward = r
        node.designer_reward = (mean_a + mean_b)/2.0
        node.behavioral_characteristics = (mean_a, mean_b)

    # add link to starting node
    G.add_edge(CustomEdge(START, config.START_NODE, [(config.START_NODE, 1-FAIL_PROB), (DEATH, FAIL_PROB)]))

    # clean nodes
    clean_graph(G)

    return G

def __reset_node(n: CustomNode):
    if n.name != Keys.START and n.name != Keys.DEATH:
        n.reward = n.designer_reward
        n.visited_count = 0
        n.percent_completable = 0

def __reset_edge(e: CustomEdge):
    e.sum_percent_complete = 0
    e.sum_visits = 0

def reset_graph(G: Graph, config: Config):
     # remove all edges to the start node
    neighbors = list(G.get_node(Keys.START).neighbors)
    while len(neighbors) != 0:
        G.remove_edge(Keys.START, neighbors.pop())
    
    G.add_edge(CustomEdge(Keys.START, config.START_NODE, [(config.START_NODE, 0.8), (Keys.DEATH, 0.2)]))

    # reset nodes and edges in the graph
    G.map_nodes(__reset_node)
    G.map_edges(__reset_edge)