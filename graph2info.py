import argparse, math, pickle, pprint, random, sys
import Utility.util as util
import networkx as nx



def print_info(graph):
    print('nodes:', len(graph.nodes))
    print('edges:', len(graph.edges))

    slice_count = 0
    for node in graph.nodes:
        slice_count += len(graph.nodes[node]['slices'])
        
    print('slices:', slice_count)
    print('slices per node:', slice_count / len(graph.nodes))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get graph info.')
    parser.add_argument('filename', type=str, help='Input graph.')
    args = parser.parse_args()

    with open(args.filename, 'rb') as f:
        graph = pickle.load(f)
    
    print_info(graph)
