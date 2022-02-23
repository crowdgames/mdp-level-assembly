from Utility import Counter

class BaseFit:
    def __init__(self, rl_agent, config, segments, playthroughs):
        self.rl_agent = rl_agent
        self.config = config
        self.segments = segments
        self.playthroughs = playthroughs
        self.counter = Counter()

    def __node_no_index(self, node):
        if '__' in node:
            return node
            
        a, b, _ = node.split(',')
        return f'{a},{b}'

    def get_level(self, node):
        lvl = []
        size = 1
        lvl += self.rl_agent.get_node_meta_data(node, 'slices')
        nodes = [node]
        lengths = [len(lvl)]
        while size < self.segments:
            node = self.rl_agent.get(node)
            self.counter.add(self.__node_no_index(node))
            nodes.append(node)
            segment = self.rl_agent.get_node_meta_data(node, 'slices')
            lvl += segment
            lengths.append(len(segment))
            size += 1 * '__' not in node # small optimization to remove branching
        
        lengths[0] += self.config.PADDING_SIZE 
        lengths[-1] += self.config.PADDING_SIZE

        return lvl, nodes, lengths

    def update_from_playthrough(self, playthrough):
        for entry in playthrough:
            node, designer_r, player_r = entry
            if '__' in node:
                max_r = self.rl_agent.get_node_meta_data(node, 'max_r')
                self.rl_agent.set_node_meta_data(
                    node, 
                    'r', 
                    player_r + max_r * designer_r / self.counter.get(node, default=1))
            else:
                a, b, _ = node.split(',')
                index = 0
                cur_node = f'{a},{b},{index}'
                node_name = self.__node_no_index(cur_node)
                while cur_node in self.rl_agent.G:
                    max_r = self.rl_agent.get_node_meta_data(node, 'max_r')
                    self.rl_agent.set_node_meta_data(
                        cur_node, 
                        'r', 
                        player_r + max_r * designer_r / self.counter.get(node_name, default=1))
                    index +=1
                    cur_node = f'{a},{b},{index}'

            entry.append(self.rl_agent.get_node_meta_data(node, 'r'))