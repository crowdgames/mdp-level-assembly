from .Keys import *

class Base:
    def __init__(self, graph, name):
        self.G = graph
        self.NAME = name

        self.__visited = set()
        self.__easiest_node = None
        self.__easiest_node_val = 10000
        self.__hardest_node = None
        self.__hardest_node_val = -10000

    def get(self, node):
        raise NotImplementedError('Caller must implement the "get" method.')

    def update(self, playthrough):
        raise NotImplementedError('Caller must implement the "update" method.')

    def increment_count(self, node):
        self.G.nodes[node][C] += 1

    def get_md(self, node, field_name):
        # get node meta data
        return self.G.nodes[node][field_name]

    def set_md(self, node, field_name, value):
        # set node meta data
        self.G.nodes[node][field_name] = value

    def add_to_visited(self, node):
        if node not in self.__visited:
            d = self.get_md(node, DR)

            if d < self.__easiest_node_val:
                self.__easiest_node_val = d
                self.__easiest_node = node

            if d > self.__hardest_node_val:
                self.__hardest_node_val = d
                self.__hardest_node = node

            self.__visited.add(node)

    def hardest_node(self):
        return self.__hardest_node, self.__hardest_node_val

    def easiest_node(self):
        return self.__easiest_node, self.__easiest_node_val

    def visited_iter(self):
        return iter(self.__visited)

