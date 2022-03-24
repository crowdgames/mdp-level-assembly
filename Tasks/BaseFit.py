from Utility.RewardType import get_reward
from Directors.Keys import *

class BaseFit:
    def __init__(self, rl_agent, config, segments, playthroughs):
        self.rl_agent = rl_agent
        self.config = config
        self.segments = segments
        self.playthroughs = playthroughs

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

    def update_from_playthrough(self, playthrough):
        for entry in playthrough.entries:
            # Set the designer reward and total reward.
            #
            #   The designer reward is the designer reward multiplied by the 
            #   percent of the level segment that the player completed all 
            #   divided by the number of times that node has been seen by the
            #   player. This division is a penalty.
            #
            #   The total reward is the sum of the designer and player reward

            c = self.rl_agent.get_md(entry.node_name, C)
            d = self.rl_agent.get_md(entry.node_name, D)
            entry.designer_reward = d * entry.percent_completable / c
            entry.total_reward = entry.designer_reward + entry.player_reward

            # update the reward based on the designer and the player
            self.rl_agent.set_md(
                entry.node_name, 
                R, 
                get_reward(self.config.REWARD_TYPE, entry.designer_reward, entry.player_reward))

            # update number of times the node has been seen
            self.rl_agent.set_md(entry.node_name, C, c+1)

           