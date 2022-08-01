from Games.Config import Config
from Games import MARIO, ICARUS
from Players.GramPlayer import GramPlayer
from Tasks import *
from Games import *
from Players.SegmentPlayers import *
from Utility import CustomEdge, Keys
from Utility.AdaptivePolicyIteration import AdaptivePolicyIteration
from Utility.CustomNode import CustomNode
from Utility.util import reset_graph
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
config = ICARUS

# set the reward type
config.REWARD_TYPE = Utility.RewardType.BOTH
REWARD_StR = Utility.reward_type_to_str(config.REWARD_TYPE)

# get Directors to use for the upcoming task
G: Graph = Utility.get_level_segment_graph(config, config.ALLOW_EMPTY_LINK)
PLAYERS = SEGMENT_PLAYERS

get_policies = []
get_policies.append(('Greedy', lambda G, player_won: greed_policy(G)))

to_run = []
for name, policy_maker in get_policies:
    for p_name, p_eval in PLAYERS.items():
        to_run.append((policy_maker, p_name, p_eval, name))
        f_name = f'player_{p_name}_game_{config.NAME}_director_{name}_reward_{REWARD_StR}.json'
        path = join(config.BASE_DIR, f_name)
        if os.path.exists(path):
            os.remove(path)

progress_bar = tqdm(to_run, leave=False, disable=False)
for rl_agent, p_name, p_eval, name in progress_bar:
    progress_bar.set_description(f'{name} :: {p_name} :: {config.NAME}')
    data = []

    for i in trange(3, leave=False, disable=False):
        # reset the graph
        G: Graph = Utility.get_level_segment_graph(config, config.ALLOW_EMPTY_LINK)
        seed(i)

        # run the agent
        task = FitPlayerPersona(
            G,
            rl_agent, 
            config, 
            5, 
            20, 
            p_eval, 
            False, 
            False)

        data.append(task.run())


