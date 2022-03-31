from Utility.RewardType import get_reward
from Directors.Keys import *

class BaseFit:
    def __init__(self, rl_agent, config, segments, playthroughs, using_segments):
        self.rl_agent = rl_agent
        self.config = config
        self.segments = segments
        self.playthroughs = playthroughs
        self.using_segments = using_segments

    def get_level(self, node):
        lvl = []
        size = 1
        lvl += self.rl_agent.get_md(node, S)
        nodes = [node]
        lengths = [len(lvl)]
        while size < self.segments:
            node = self.rl_agent.get(node)
            nodes.append(node)
            segment = self.rl_agent.get_md(node, S)
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
            nodes.append(node)
            size += 1 * '__' not in node # small optimization to remove branching

        return nodes

    def __get_cell_nodes(self, node, graph):
        if '__' in node or '(' in node: # link or tuple
            return [node]
            
        a, b, _ = node.split(',')
        i = 0
        nodes = [f'{a},{b},{i}']
        while nodes[-1] in graph.nodes:
            i += 1
            nodes.append(f'{a},{b},{i}')

        nodes.pop() 
        return nodes

    def update_from_playthrough(self, playthrough):
        for e in playthrough.entries:
            # Set the designer reward and total reward.
            #
            #   The designer reward is the designer reward multiplied by the 
            #   percent of the level segment that the player completed all 
            #   divided by the number of times that node has been seen by the
            #   player. This division is a penalty.
            #
            #   The total reward is the sum of the designer and player reward
            c = self.rl_agent.get_md(e.node_name, C)
            d = self.rl_agent.get_md(e.node_name, D)

            e.designer_reward = (d * e.percent_completable) / c
            e.total_reward = e.designer_reward + e.player_reward
            e.reward = get_reward(self.config.REWARD_TYPE, e)

            # update the reward based on the designer and the player
            self.rl_agent.set_md(e.node_name, R, e.reward)

            # update number of times every node has been seen for every elite
            # in the same cell as the node in the entry.  
            if self.using_segments:
                new_count = c+1  
                for node in self.__get_cell_nodes(e.node_name, self.rl_agent.G):
                    self.rl_agent.set_md(node, C, new_count)
                    if node != e.node_name:
                        r = self.rl_agent.get_md(node, R)
                        self.rl_agent.set_md(node, R, r/new_count)

           