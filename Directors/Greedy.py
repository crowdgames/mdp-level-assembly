from .Base import Base
from .Keys import *

from collections import namedtuple


Node = namedtuple('Node', ['size', 'reward', 'nodes'])

class Greedy(Base):
    def __init__(self, graph):
        super().__init__(graph, 'Greedy')

    def update(self, _):
        pass

    def __size(self, node):
        return '__' not in node

    def get(self, node, k):
        best = Node(0, 0, None)
        queue = [Node(1, self.get_md(node, R), [node])]
        # for n in self.G.neighbors(node):
        #     r = self.get_md(n, R)
        #     queue.append(Node(self.__size(n), r, [n]))

        #     if r > best.reward:
        #         best = queue[-1]

        while len(queue) != 0:
            cur = queue.pop()
            for n in self.G.neighbors(cur.nodes[-1]):
                size = cur.size + self.__size(n)
                reward = cur.reward + self.get_md(n, R)
                nodes = cur.nodes + [n,]
                new_node = Node(size, reward, nodes)
                
                if size > k:
                    pass
                elif size == k:
                    if reward > best.reward:
                        best = new_node
                else:
                    queue.append(new_node)

        return best.nodes
    
    def get_starting_node(self):
        best_n = None
        best_r = 0
        for n in self.visited_iter():
            r = self.get_md(n, R)
            if r > best_r:
                best_r = r
                best_n = n

        return best_n
