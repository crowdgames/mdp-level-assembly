import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from copy import copy

from Games import *
import Utility
from os import listdir, mkdir
from os.path import join, isdir
from json import load
from glob import glob
import os
import sys



config = Icarus
# G,_ = Utility.get_n_gram_graph(config)

# nx.draw(G, pos = nx.nx_pydot.graphviz_layout(G), \
#     node_size=1200, node_color='lightblue', linewidths=0.25, \
#     font_size=10, font_weight='bold', with_labels=True, dpi=1000)
# plt.show()

full_graph = Utility.get_level_segment_graph(config, True)

compressed_graph = nx.DiGraph()
links = []
for n in full_graph.nodes:
    if '__' in n:
        links.append(n)

for l in links:
    src, tgt = l.split('__')
    full_graph.remove_node(l)
    full_graph.add_edge(src, tgt)

labeldict = {}
pos_nodes = {}
for n in full_graph.nodes:
    a,b,_=n.split(',')
    compressed_graph.add_node(f'{a},{b}', pos=(int(a), int(b)))
    labeldict[f'{a},{b}'] = f'{full_graph.nodes[n]["R"]:0.02f}'
    pos_nodes[f'{a},{b}'] = (int(a)+0.3,int(b)-0.4)

for src, tgt in full_graph.edges:
    src_a, src_b, _ = src.split(',')
    tgt_a, tgt_b, _ = tgt.split(',')
    compressed_graph.add_edge(f'{src_a},{src_b}', f'{tgt_a},{tgt_b}')
    

pos = nx.get_node_attributes(compressed_graph, 'pos')

color_map = []
for res in compressed_graph.in_degree():
    node_key, in_edges = res
    if in_edges == 0:
        color_map.append('gray')
    elif compressed_graph.out_degree(node_key) == 0:
        color_map.append('green')
    else:
        color_map.append('brown')


plt.figure(figsize=(15,15))
# plt.xlim(min_cor, max_cor)
# plt.ylim(min_cor, max_cor)

nx.draw(compressed_graph, pos, node_color=color_map, node_size=60, with_labels=False, arrowsize=15)
nx.draw_networkx_labels(compressed_graph, pos=pos_nodes, labels=labeldict) 

save_path = os.path.join('figure', f'{config.NAME}_compressed_graph.pdf')

print(f'Saving to: {save_path}')
plt.savefig(save_path, bbox_inches="tight") 

# save_path = os.path.join('figure', f'dda_grid_{config.NAME}.pdf')
# for src in data:
#     x,y,_ = src.split(',')
#     x = int(x)
#     y = int(y)

#     pos = (x,y)
#     if pos in seen:
#         continue
#     else:
#         seen.add(pos)

#     index = 0
#     k = f'{x},{y},{index}'
#     keys = []
#     while k in data:
#         keys.append(k)
#         index += 1
#         k = f'{x},{y},{index}'

#     x_points.append(x)
#     y_points.append(y)
#     graph.add_node(pos, pos=pos)

#     for k in keys:
#         for dst in data[k]:
#             if data[k][dst][algorithm_name]['percent_playable'] == 1.0:
#                 dst_x,dst_y,_ = dst.split(',')
#                 dst_pos = (int(dst_x), int(dst_y))
#                 if not graph.has_node(dst_pos):
#                     graph.add_node(dst_pos, pos=dst_pos)

#                 graph.add_edge(pos, dst_pos)

# color_map = []
# for res in graph.in_degree():
#     node_key, in_edges = res
#     if in_edges == 0:
#         color_map.append('gray')
#     elif graph.out_degree(node_key) == 0:
#         color_map.append('green')
#     else:
#         color_map.append('brown')

# min_cor = min(min(x_points), min(y_points)) - 1
# max_cor = max(max(x_points), max(y_points)) + 1

# pos = nx.get_node_attributes(graph, 'pos')
# plt.figure(figsize=(15,15))
# plt.xlim(min_cor, max_cor)
# plt.ylim(min_cor, max_cor)

# nx.draw(graph, pos, node_color=color_map, node_size=60, with_labels=False, arrowsize=15) 


# nodes = nx.draw_networkx_nodes(graph, pos, node_size=60, node_color=color_map)
# edges = nx.draw_networkx_edges(
#     graph,
#     pos,
#     node_size=20,
#     arrowstyle="->",
#     arrowsize=10,
#     edge_color=edge_colors,
#     edge_cmap=cmap,
#     width=2,
# )
# plt.show()
# print(f'Saving to: {save_path}')
# plt.savefig(save_path, bbox_inches="tight") 


# nodes = set()
# for path in list(nx.bfs_edges(graph, '(0, 0)')):
#     for n in path:
#         nodes.add(n)

# file_path = os.path.join(sys.argv[1], 'info.txt')
# if os.path.exists(file_path):
#     f = open(file_path, 'a')
# else:
#     f = open(file_path, 'w')

# f.write(f'\n\nDDA Grid {sys.argv} Results\n')
# f.write(f'Connected nodes: {len(nodes)}\n')
# f.write(f'Total number of nodes: {len(graph.nodes)}\n')
# f.close()
