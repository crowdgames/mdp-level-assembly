import argparse, pickle, math, pprint, random, sys
import util
import networkx as nx



def gen_level(graph, size):
    curr_node = random.sample(graph.nodes, 1)[0]
    slices_out = graph.nodes[curr_node]['slices']

    while len(slices_out) < size:
        out_edges = list(graph.out_edges(curr_node))

        curr_node = util.select_random_next(graph, out_edges)
        slices_out += graph.nodes[curr_node]['slices']

    return util.slices_to_rows(slices_out, graph.graph['transpose'])



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple n-grams.')
    parser.add_argument('filename', type=str, help='Input graph file.')
    parser.add_argument('--size', type=int, required=True, help='Generate level of minimum size.')
    args = parser.parse_args()

    with open(args.filename, 'rb') as f:
        graph = pickle.load(f)

    level = gen_level(graph, args.size)
    util.print_level(level)
