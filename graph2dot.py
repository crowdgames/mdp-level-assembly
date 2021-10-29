import argparse, math, pickle, pprint, random, sys
import util
import networkx as nx



def slices_to_display(slices, transpose):
    return '\\n'.join(util.slices_to_rows(slices, transpose))

def print_graph_dot(graph):
    print('digraph G {')
    print('  graph [fontname="courier", splines="spline", overlap="false"];')
    print('  node [fontname="courier", shape="box"];')
    print('  edge [fontname="courier"];')
    for nid in graph.nodes:
        slices =  graph.nodes[nid]['slices'] if 'slices' in graph.nodes[nid] else []
        label = slices_to_display(slices, graph.graph['transpose'])
        
        fillcolor = '#eeeeee'
        if len(graph.in_edges(nid)) == 0:
            fillcolor = '#555555'
        if len(graph.out_edges(nid)) == 0:
            fillcolor = '#555555'

        print('  "%s" [label="%s"; style="filled"; fillcolor="%s"];' % (nid, label, fillcolor))

    for ea, eb in graph.edges:
        print('  "%s" -> "%s";' % (ea, eb))
    
    print('}')




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create dot file.')
    parser.add_argument('filename', type=str, help='Input graph.')
    args = parser.parse_args()

    with open(args.filename, 'rb') as f:
        graph = pickle.load(f)
    
    print_graph_dot(graph)
