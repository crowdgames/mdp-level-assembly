from Players.Playthrough import Playthrough
from Utility.CustomNode import CustomNode
from Utility.RewardType import set_reward
from Utility import CustomEdge, Keys

from typing import Callable, Dict, List
from GDM.Graph import Graph
from tqdm import trange

class BaseFit:
    def __init__(
            self, 
            graph: Graph, 
            director: Callable[[Graph], 
            Dict[str, str]], 
            config, 
            segments: int, 
            playthroughs: int, 
            using_segments: bool, 
            hide_tqdm: bool):

        self.G = graph
        self.director = director
        self.config = config
        self.segments = segments
        self.playthroughs = playthroughs
        self.using_segments = using_segments
        self.hide_tqdm = hide_tqdm

        self.pi = director(self.G, True)

    def get_level(self):
        lvl = []
        node = Keys.START
        lvl = []
        nodes = []
        lengths = []
        while len(lengths) < self.segments:
            node = self.pi[node]
            nodes.append(node)
            segment = self.G.get_node(node).slices
            lvl += segment
            lengths.append(len(segment))
        
        lengths[0] += self.config.PADDING_SIZE 
        lengths[-1] += self.config.PADDING_SIZE

        return lvl, nodes, lengths

    def __get_cell_nodes(self, node: str) -> List[str]:
        if '__' in node or '(' in node: # link or tuple
            return [node]
            
        a, b, _ = node.split(',')
        i: int = 0
        nodes: List[str] = [f'{a},{b},{i}']
        while self.G.has_node(nodes[-1]):
            i += 1
            nodes.append(f'{a},{b},{i}')

        nodes.pop() 
        return nodes
        
    def _fit(self, data, player_persona: Callable[[Graph, List[str], float], Playthrough], num_playthroughs):
        for _ in trange(num_playthroughs, leave=False, disable=self.hide_tqdm):
            if self.need_full_level:
                # an agent is going to play the game
                lvl, nodes, lengths = self.get_level()
                assert self.config.GRAM.sequence_is_possible(lvl)
                playthrough = player_persona(lvl, nodes, None)
            else:
                # surrogate is going to play the game   
                nodes = [Keys.START]
                size = 1
                while size < self.segments + 1:
                    nodes.append(self.pi[nodes[-1]])
                    size += 1 * '__' not in nodes[-1] # small optimization to remove branching

                nodes.pop(0)
                playthrough = player_persona(self.G, nodes, self.config.NUM_BC)

            # Update the graph rewards based on the playthrough. Playthrough 
            # entries are also updated with important details for logging.
            previous_node = Keys.START
            tgt_nodes_to_update = set()

            for e in playthrough.entries:
                tgt_nodes_to_update.add(e.node_name)

                # update visited
                if '__' not in e.node_name and e.percent_completable == 1.0:
                    if not self.G.has_edge(Keys.START, e.node_name):
                        # this is updated below
                        self.G.add_edge(CustomEdge(Keys.START, e.node_name, [(e.node_name, 1.0), (Keys.DEATH, 0.0)]))
                
                # update graph values
                node: CustomNode = self.G.get_node(e.node_name)
                node.percent_completable = e.percent_completable
                node.player_reward = e.player_reward
                node.visited_count += 1

                set_reward(self.config.REWARD_TYPE, node)

                # update playthrough entry
                e.designer_reward = node.designer_reward
                e.total_reward = node.reward
                e.reward = node.reward

                # update edge
                edge: CustomEdge = self.G.get_edge(previous_node, e.node_name)
                edge.sum_visits += 1
                edge.sum_percent_complete += e.percent_completable
                previous_node = e.node_name

                # update number of times every node has been seen for every elite
                # in the same cell as the node in the entry.  
                for new_node_name in self.__get_cell_nodes(e.node_name):
                    new_node = self.G.get_node(new_node_name)
                    new_node.visited_count = node.visited_count
                    if new_node_name != e.node_name:
                        set_reward(self.config.REWARD_TYPE, new_node)
            
            # update edge probabilities
            for tgt_node in tgt_nodes_to_update:
                source_nodes = []
                sum_percent_complete: float = 1
                sum_visited: int = 1
                edge: CustomEdge
                for edge in self.G.edges.values():
                    if edge.tgt == tgt_node:
                        sum_percent_complete += edge.sum_percent_complete
                        sum_visited += edge.sum_visits
                        source_nodes.append(edge.src)

                win_prob = sum_percent_complete / sum_visited
                death_prob = 1 - win_prob
                for src_node in source_nodes:
                    self.G.get_edge(src_node, tgt_node).probability = [(tgt_node, win_prob), (Keys.DEATH, death_prob)]

            # Update based on new graph values
            player_won = len(nodes) == len(playthrough.entries) and playthrough.entries[-1].percent_completable == 1.0
            self.pi = self.director(self.G, player_won)
            # start_edges = self.G.neighbors(Keys.START)
            # temp = [self.G.get_node(n) for n in tgt_nodes_to_update]

            # output data is updated 
            data.append(playthrough.get_summary(nodes))