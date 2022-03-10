from Utility import Counter
from Utility.RewardType import get_reward

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

    def get_level_nodes(self, node):
        nodes = [node]
        size = 1

        while size < self.segments:
            node = self.rl_agent.get(node)
            self.counter.add(self.__node_no_index(node))
            nodes.append(node)
            size += 1 * '__' not in node # small optimization to remove branching

        return nodes

    def update_from_playthrough(self, playthrough):
        '''
        This updates the rewards in the graph and the reward post the
        playthrough is added to each playthrough entry
        '''
        for entry in playthrough:
            node, compleatability, player_r = entry

            # add design reward and total reward to playthrough for future
            # analysis. Not strictly necessary but it's a better life.
            entry.append(self.rl_agent.get_node_meta_data(node, 'design_r'))
            entry.append(entry[-1] + player_r)

            # update node meta data for future rewards
            if '__' in node:
                # for a link node we update only that node
                max_r = self.rl_agent.get_node_meta_data(node, 'max_r')
                design_r = max_r * compleatability / self.counter.get(node, default=1)

                self.rl_agent.set_node_meta_data(node, 'r', get_reward(self.config.REWARD_TYPE, design_r, player_r))
                self.rl_agent.set_node_meta_data(node, 'design_r', design_r)
            else:
                # for regular nodes we update it and all of its associated nodes by 
                # looping through possible indexes till one that does not exist is
                # found. This makes it so the player is less likely to see levels
                # that are like what they have already played.
                a, b, _ = node.split(',')
                index = 0
                cur_node = f'{a},{b},{index}'
                node_name = self.__node_no_index(cur_node)
                while cur_node in self.rl_agent.G:
                    max_r = self.rl_agent.get_node_meta_data(node, 'max_r')
                    design_r = max_r * compleatability / self.counter.get(node_name, default=1)

                    self.rl_agent.set_node_meta_data(cur_node, 'r', get_reward(self.config.REWARD_TYPE, design_r, player_r))
                    self.rl_agent.set_node_meta_data(cur_node, 'design_r', design_r)
                    
                    index +=1
                    cur_node = f'{a},{b},{index}'

           