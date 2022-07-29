from Games.Config import Config
from Players.GramPlayer import GramPlayer
from Tasks import *
from Games import *
from Players.SegmentPlayers import *
from Utility import CustomEdge, Keys
from Utility.CustomNode import CustomNode
SEGMENT_PLAYERS = PLAYERS
from Tasks.FitPlayerPersona import FitPlayerPersona
import Utility

from GDM.Baseline import random_policy, greed_policy
from GDM.ADP import policy_iteration, value_iteration

from os.path import join
from random import seed
from time import time
from pickle import dump as pkl_dump
from json import dump as json_dump
from tqdm import tqdm, trange
import argparse
import os

from Utility.RewardType import RewardType

'''
TODO: the G needs a starting node
TODO: starting node needs to be connected to first node at the start
TODO: starting node needs all edges removed except the easiest node
TODO: handle when the fail node is reached
'''


start = time()

# Get Game 
config: Config 
config = MARIO

# set the reward type
config.REWARD_TYPE = Utility.RewardType.BOTH
REWARD_StR = Utility.reward_type_to_str(config.REWARD_TYPE)

# get Directors to use for the upcoming task
G, gram = Utility.get_n_gram_graph(config)
config.GRAM = gram
PLAYERS = {
    'agent': GramPlayer(config).get
}
# G: Graph = Utility.get_level_segment_graph(config, config.ALLOW_EMPTY_LINK)
# PLAYERS = SEGMENT_PLAYERS


get_policies = []
# get_policies.append(('Policy', lambda G: policy_iteration(G, 0.9, modified=True, in_place=True, policy_k=20)))
# get_policies.append(('Value', lambda G: value_iteration(G, args.max_iter, args.gamma, args.theta, in_place=True)))
get_policies.append(('Greedy', lambda G, player_won: greed_policy(G)))
# get_policies.append(('Random', lambda G: random_policy(G)))

to_run = []
for name, policy_maker in get_policies:
    for p_name, p_eval in PLAYERS.items():
        to_run.append((policy_maker, p_name, p_eval, name))

progress_bar = tqdm(to_run, leave=False, disable=True)
for rl_agent, p_name, p_eval, name in progress_bar:
    progress_bar.set_description(f'{name} :: {p_name} :: {config.NAME}')
    data = []

    # run
    for i in trange(3, leave=False, disable=True):
        # remove all edges to the start node
        neighbors = list(G.get_node(Keys.START).neighbors)
        while len(neighbors) != 0:
            G.remove_edge(Keys.START, neighbors.pop())
        
        G.add_edge(CustomEdge(Keys.START, config.START_NODE, [(config.START_NODE, 0.8), (Keys.DEATH, 0.2)]))

        # reset nodes and edges in the graph
        def reset_node(n: CustomNode):
            if n.name != Keys.START and n.name != Keys.DEATH:
                n.reward = n.designer_reward
                n.visited_count = 0
                n.percent_completable = 0

        def reset_edge(e: CustomEdge):
            e.sum_percent_complete = 0
            e.sum_visits = 0
                
        G.map_nodes(reset_node)
        G.map_edges(reset_edge)
        
        seed(i)
        task = FitPlayerPersona(
            G,
            rl_agent, 
            config, 
            5, 
            50, # playthroughs 
            p_eval, 
            True, 
            True)

        data.append(task.run())


