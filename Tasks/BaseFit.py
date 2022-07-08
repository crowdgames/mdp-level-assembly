from Utility.RewardType import set_reward
from Directors.Keys import *

from tqdm import trange

class BaseFit:
    def __init__(self, director, config, segments, playthroughs, using_segments, hide_tqdm):
        self.director = director
        self.config = config
        self.segments = segments
        self.playthroughs = playthroughs
        self.using_segments = using_segments
        self.hide_tqdm = hide_tqdm

    def get_level(self, node):
        lvl = []
        size = 1
        lvl += self.director.get_md(node, S)
        nodes = [node]
        lengths = [len(lvl)]
        while size < self.segments:
            node = self.director.get(node)
            nodes.append(node)
            segment = self.director.get_md(node, S)
            lvl += segment
            lengths.append(len(segment))
            size += 1 * '__' not in node # small optimization to remove branching
        
        lengths[0] += self.config.PADDING_SIZE 
        lengths[-1] += self.config.PADDING_SIZE

        return lvl, nodes, lengths

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
        
    def _fit(self, cur, data, player_persona, num_playthroughs):
        for _ in trange(num_playthroughs, leave=False, disable=self.hide_tqdm):
            if self.need_full_level:
                # an agent is going to play the game
                lvl, nodes, lengths = self.get_level(cur)
                playthrough = player_persona(lvl, nodes, lengths)
                assert self.config.GRAM.sequence_is_possible(lvl)
            else:
                # surrogate is going to play it
                nodes = self.director.get(cur, self.segments)
                playthrough = player_persona(nodes, self.director, self.config.NUM_BC)

            # Update the graph rewards based on the playthrough. Playthrough 
            # entries are also updated with important details for logging.
            for e in playthrough.entries:
                # update visited
                if '__' not in e.node_name and e.percent_completable == 1.0:
                    self.director.add_to_visited(e.node_name)
                
                # update graph values
                node = e.node_name
                self.director.set_md(node, PC, e.percent_completable)
                self.director.set_md(node, PR, e.player_reward)
                COUNT = self.director.get_md(node, C) + 1
                self.director.set_md(node, C, COUNT)
                set_reward(self.config.REWARD_TYPE, self.director.G, node)

                # update playthrough entry
                e.designer_reward = self.director.get_md(node, DR)
                e.total_reward = self.director.get_md(node, TR)
                e.reward = self.director.get_md(node, TR)

                # update number of times every node has been seen for every elite
                # in the same cell as the node in the entry.  
                for node in self.__get_cell_nodes(e.node_name, self.director.G):
                    self.director.set_md(node, C, COUNT)
                    if node != e.node_name:
                        set_reward(self.config.REWARD_TYPE, self.director.G, node)

            # rl agent learns from the playthrough
            self.director.update(playthrough)

            # get next starting node
            cur = self.director.get_starting_node()

            # make sure the node in question is not a link. If it is then go to the 
            # next node.
            if '__' in cur:
                cur = cur.split('__')[1]

            # output data is updated 
            data.append(playthrough.get_summary(nodes))

        return cur






    # # dead code
    # def __get_starting_node(self, playthrough):
    #     player_won = all([e.percent_completable == 1.0 for e in playthrough.entries])

    #     # get hardest node the player played through
    #     e = playthrough.entries[-1]
    #     hn_key = e.node_name
    #     hn_val = self.director.get_md(hn_key, DR)

    #     node = None
    #     if player_won:
    #         # If the player won, find the next hardest node. I do think using a
    #         # a selection based on a Pareto frontier would be more interesting.
    #         node = self.director.get(hn_key)
    #     else:
    #         # else, pick a node in between the easiest and hardest node that the
    #         # player has already visited
    #         en_key, en_val = self.director.easiest_node()
    #         tgt = (en_val + hn_val) / 2.0
    #         best_val = abs(tgt - en_val)
    #         node = en_key

    #         for n in self.director.visited_iter():
    #             val = self.director.get_md(n, DR)
    #             diff = abs(tgt - val)
    #             if diff < best_val:
    #                 best_val = diff
    #                 node = n

    #     return node