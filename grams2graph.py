import argparse, pickle, math, pprint, random, sys
import util
import networkx as nx



def construct_graph(filenames, gramsize, transpose):
    slices_to_out = {}
    for filename in filenames:
        with open(filename) as infile:
            lines = [_.strip() for _ in infile.readlines()]

        slices = util.rows_to_slices(lines, transpose)

        for igram in range(gramsize - 1, len(slices)):
            left = tuple(slices[igram - (gramsize - 1):igram])
            right = slices[igram]

            if left not in slices_to_out:
                slices_to_out[left] = []
            slices_to_out[left].append(right)

    src_dst = []
    slices_to_nid = {}
    for src, right_options in slices_to_out.items():
        for right_option in right_options:
            dst = src[1:] + (right_option,)

            if src not in slices_to_nid:
                slices_to_nid[src] = str(len(slices_to_nid) + 1)
            if dst not in slices_to_nid:
                slices_to_nid[dst] = str(len(slices_to_nid) + 1)

            src_dst.append((src, dst))

    graph = nx.DiGraph()
    graph.graph['transpose'] = transpose

    for src, dst in src_dst:
        srci = slices_to_nid[src]
        dsti = slices_to_nid[dst]
        graph.add_node(srci, slices_gram=src)
        graph.add_node(dsti, slices_gram=dst)
        
        graph.nodes[srci]['slices'] = src[-1:]
        graph.nodes[dsti]['slices'] = dst[-1:]
        
        if not graph.has_edge(srci, dsti):
            graph.add_edge(srci, dsti, weight=1)

        else:
            graph.edges[(srci, dsti)]['weight'] += 1

    graph = util.largest_scc(graph)

    return graph



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple n-grams.')
    parser.add_argument('filenames', type=str, nargs='+', help='Input level files.')
    parser.add_argument('--gramsize', type=int, required=True, help='N-gram size.')
    parser.add_argument('--transpose', action='store_true', help='Transpose level to use rows instead of columns.')
    parser.add_argument('--out', type=str, required=True, help='File to write to.')
    args = parser.parse_args()

    graph = construct_graph(args.filenames, args.gramsize, args.transpose)

    with open(args.out, 'wb') as f:
        pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)
