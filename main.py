from Games.Config import Config
from Games import MARIO, ICARUS
from Players.GramPlayer import GramPlayer
from Tasks import *
from Games import *
from Players.SegmentPlayers import *
from Utility import CustomEdge, Keys
from Utility.AdaptivePolicyIteration import AdaptivePolicyIteration
from Utility.CustomNode import CustomNode
from Utility.Math import median
from Utility.util import reset_graph
SEGMENT_PLAYERS = PLAYERS
from Tasks.FitPlayerPersona import FitPlayerPersona
import Utility

from GDM.Baseline import random_policy, greed_policy
from GDM.ADP import policy_iteration

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

parser = argparse.ArgumentParser(description='Graph Procedural Content Generation via Reinforcement Learning')
parser.add_argument('--seed', type=int, default=0, help='Set seed for generation')

game_group = parser.add_mutually_exclusive_group(required=True)
game_group.add_argument('--dungeongram', action='store_true', help='Run DungeonGrams')
game_group.add_argument('--mario', action='store_true', help='Run Mario')
game_group.add_argument('--icarus', action='store_true', help='Run Icarus')

task_group = parser.add_mutually_exclusive_group(required=True)
task_group.add_argument('--fit-persona', action='store_true', help='Fit to a player persona')
task_group.add_argument('--switch-persona', action='store_true', help='Fit to two player personas')
task_group.add_argument('--get-level', action='store_true', help='Generate a level with a G trained with --fit-to-agent')
task_group.add_argument('--v-n-gram', action='store_true', help='get n-gram visualizations')
task_group.add_argument('--stats', action='store_true', help='get stats on the graph')

G_group = parser.add_mutually_exclusive_group(required=True)
G_group.add_argument('--segment-graph', action='store_true', help='segment based generation for G')
G_group.add_argument('--n-gram-graph', action='store_true', help='n-gram based generation for G')

rl_agent_group = parser.add_mutually_exclusive_group(required=True)
rl_agent_group.add_argument('--policy', action='store_true', help='Policy Iteration Agent')
rl_agent_group.add_argument('--adaptive-policy', action='store_true', help='Adaptive Policy Iteration Agent')
rl_agent_group.add_argument('--random', action='store_true', help='Randomly choose where to go regardless of the player')
rl_agent_group.add_argument('--greedy', action='store_true', help='Greedily choose where to go based on the reward')
rl_agent_group.add_argument('--all', action='store_true', help='Run every agent')

reward_group = parser.add_mutually_exclusive_group(required=True)
reward_group.add_argument('--r-player', action='store_true', help='reward based on player only.')
reward_group.add_argument('--r-designer', action='store_true', help='reward based on designer only.')
reward_group.add_argument('--r-both', action='store_true', help='reward based on both designer and player only.')

parser.add_argument('--segments', type=int, default=3, help='Number of segments to fit together')
parser.add_argument('--theta', type=float, default=1e-13, help='Convergence criteria for Ialue Iteration')
parser.add_argument('--max-iter', type=int, default=500, help='Max # of iterations for Value Iteration')
parser.add_argument('--policy-iter', type=int, default=20, help='# of iterations for Policy Evaluation step')
parser.add_argument('--gamma', type=float, default=0.95, help='Discount factor for all RL algorithms')
parser.add_argument('--runs', type=int, default=100, help='Number of runs for a person when --fit-person is used')
parser.add_argument('--playthroughs', type=int, default=20, help='Number of levels played per director')
parser.add_argument('--hide-tqdm', action='store_true', help='Hide tqdm bars')

args = parser.parse_args()
args.hide_tqdm != args.hide_tqdm

# Get Game 
config: Config 
if args.mario:
    config = MARIO
elif args.icarus:
    config = ICARUS
else:
    print('Unrecognized game type')
    import sys
    sys.exit(-1)

# set the reward type
if args.r_player:
    config.REWARD_TYPE = Utility.RewardType.PLAYER
elif args.r_designer:
    config.REWARD_TYPE = Utility.RewardType.DESIGNER
elif args.r_both:
    config.REWARD_TYPE = Utility.RewardType.BOTH

REWARD_StR = Utility.reward_type_to_str(config.REWARD_TYPE)

# get Directors to use for the upcoming task
if args.segment_graph:
    G: Graph = Utility.get_level_segment_graph(config, config.ALLOW_EMPTY_LINK)
    PLAYERS = SEGMENT_PLAYERS
else:
    G, gram = Utility.get_n_gram_graph(config)
    PLAYERS = {
        'agent': GramPlayer(config).get
    }

    config.GRAM = gram

get_policies = []
if args.policy or args.all:
    get_policies.append(('Policy', lambda G, player_won: policy_iteration(G, args.gamma, modified=True, in_place=True, policy_k=args.policy_iter)))
if args.adaptive_policy or args.all:
    api = AdaptivePolicyIteration(args.gamma, args.policy_iter)
    get_policies.append(('Adaptive Policy', lambda G, player_won: api.get_policy(G, player_won)))
if args.random or args.all:
    get_policies.append(('Greedy', lambda G, player_won: greed_policy(G)))
if args.greedy or args.all:
    get_policies.append(('Random', lambda G, player_won: random_policy(G)))

if args.fit_persona:
    to_run = []
    for name, policy_maker in get_policies:
        for p_name, p_eval in PLAYERS.items():
            to_run.append((policy_maker, p_name, p_eval, name))
            f_name = f'player_{p_name}_game_{config.NAME}_director_{name}_reward_{REWARD_StR}.json'
            path = join(config.BASE_DIR, f_name)
            if os.path.exists(path):
                os.remove(path)

    progress_bar = tqdm(to_run, leave=False, disable=args.hide_tqdm)
    for rl_agent, p_name, p_eval, name in progress_bar:
        progress_bar.set_description(f'{name} :: {p_name} :: {config.NAME}')
        data = []

        for i in trange(args.runs, leave=False, disable=args.hide_tqdm):
            # reset the graph
            if args.segment_graph:
                start = time()
                G: Graph = Utility.get_level_segment_graph(config, config.ALLOW_EMPTY_LINK)
            else:
                G, gram = Utility.get_n_gram_graph(config)
            seed(args.seed+i)

            # run the agent
            task = FitPlayerPersona(
                G,
                rl_agent, 
                config, 
                args.segments, 
                args.playthroughs, 
                p_eval, 
                args.n_gram_graph, 
                args.hide_tqdm)

            data.append(task.run())

        # create data structure and store it to a json file
        res = {
            'data': data,
            'info': {
                'seed': args.seed,
                'segments': args.segments,
                'theta': args.theta,
                'max_iter': args.max_iter,
                'policy_iter': args.policy_iter,
                'gamma': args.gamma,
                'runs': args.runs,
                'playthroughs': args.playthroughs
            }
        }

        f_name = f'player_{p_name}_game_{config.NAME}_director_{name}_reward_{REWARD_StR}.json'
        with open(join(config.BASE_DIR, f_name), 'w') as f:
            json_dump(res, f, indent=2)

elif args.switch_persona:
    for name, get_policy in tqdm(get_policies, leave=False, disable=args.hide_tqdm):
        f_name = f'switch_game_{config.NAME}_director_{name}_reward_{REWARD_StR}.json'
        if os.path.exists(join(config.BASE_DIR, f_name)):
            os.remove(join(config.BASE_DIR,f_name))

        data = []
        for i in trange(args.runs, leave=False, disable=args.hide_tqdm):
            # reset the graph
            if args.segment_graph:
                G: Graph = Utility.get_level_segment_graph(config, config.ALLOW_EMPTY_LINK)
            else:
                G, gram = Utility.get_n_gram_graph(config)
            seed(args.seed+i)

            players = [
                good_player_likes_hard_levels,
                bad_player_likes_easy_levels,
            ]

            task = SwitchPlayerPersona(
                G,
                get_policy, 
                config, 
                args.segments, 
                args.playthroughs, 
                players, 
                args.n_gram_graph,
                args.hide_tqdm)

            data.append(task.run())

        res = {
            'data': data,
            'info': {
                'seed': args.seed,
                'segments': args.segments,
                'theta': args.theta,
                'max_iter': args.max_iter,
                'policy_iter': args.policy_iter,
                'gamma': args.gamma,
                'runs': args.runs,
                'playthroughs': args.playthroughs,
                'players': [
                    'Good Player Likes Hard Levels',
                    'Bad Player Likes Easy Levels',
                ]
            }
        }

        f_name = f'switch_game_{config.NAME}_director_{name}_reward_{REWARD_StR}.json'
        with open(join(config.BASE_DIR, f_name), 'w') as f:
            json_dump(res, f, indent=2)

elif args.get_level:
    raise NotImplementedError('--get-level is not yet implemented')

elif args.v_n_gram:
    Visualization.GetNGramLevels(config, get_policies).run()

elif args.stats:
    if args.segment_graph:
        G: Graph = Utility.get_level_segment_graph(config, config.ALLOW_EMPTY_LINK)
    else:
        G, gram = Utility.get_n_gram_graph(config)

    num_nodes = sum(1 for n in G.nodes.values() if '__' not in n.name) - 2
    n: CustomNode
    connections = [len(n.neighbors) for n in G.nodes.values() if '__' not in n.name]

    print(f'Nodes: {num_nodes}')
    print()
    print(f'Min: {min(connections)}')
    print(f'Mean: {sum(connections)/num_nodes}')
    print(f'Median: {median(connections)}')
    print(f'Max: {max(connections)}')


end = time()

hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

# mac only
os.popen('say "Done!"')
print('Done!')