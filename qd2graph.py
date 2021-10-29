import argparse, json, pickle, math, pprint, random, sys
import util
import networkx as nx



def construct_graph(folder, transpose):
    with open(folder + '/dda_graph.json', 'rb') as f:
        data = json.load(f)

    graph = nx.DiGraph()
    graph.graph['transpose'] = transpose

    for node, next_data in data.items():
        node_filename = folder + '/levels/' + node.replace(',', '_') + '.txt'
        with open(node_filename, 'rt') as infile:
            lines = [_.strip() for _ in infile.readlines()]

        slices = tuple(util.rows_to_slices(lines, transpose))
        
        graph.add_node(node, slices=slices)

        for next_node, edge_data in next_data.items():
            edge_slices = tuple(edge_data['shortest']['link'])
            if len(edge_slices) == 0:
                continue

            if (node, next_node) in graph.edges:
                raise RuntimeError('Duplicate edge.')

            edge_node = node + '__' + next_node
            
            graph.add_node(edge_node, slices=edge_slices)
            graph.add_edge(node, edge_node, weight=1)
            graph.add_edge(edge_node, next_node, weight=1)

    graph = util.largest_scc(graph)

    return graph



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='QD graph.')
    parser.add_argument('folder', type=str, help='Input folder.')
    parser.add_argument('--transpose', action='store_true', help='Transpose level to use rows instead of columns.')
    parser.add_argument('--out', type=str, required=True, help='File to write to.')
    args = parser.parse_args()

    graph = construct_graph(args.folder, args.transpose)

    with open(args.out, 'wb') as f:
        pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)