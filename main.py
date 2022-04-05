from copy import deepcopy
from Players.GramPlayer import GramPlayer
from Tasks import *
from Games import *
from Players.SegmentPlayers import *
SEGMENT_PLAYERS = PLAYERS
from Tasks.FitPlayerPersona import FitPlayerPersona
import Utility
import Directors

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
TODO:

- n-gram based generation
- probability update
    - MDP
    - Q
    - greedy
'''

start = time()

parser = argparse.ArgumentParser(description='Graph Procedural Content Generation via Reinforcement Learning')
parser.add_argument('--seed', type=int, default=0, help='Set seed for generation')

game_group = parser.add_mutually_exclusive_group(required=True)
game_group.add_argument('--dungeongram', action='store_true', help='Run DungeonGrams')
game_group.add_argument('--mario', action='store_true', help='Run Mario')
game_group.add_argument('--icarus', action='store_true', help='Run Icarus')

task_group = parser.add_mutually_exclusive_group(required=True)
task_group.add_argument('--fit-agent', action='store_true', help='Fit to an agent')
task_group.add_argument('--fit-persona', action='store_true', help='Fit to a player persona')
task_group.add_argument('--switch-persona', action='store_true', help='Fit to two player personas')
task_group.add_argument('--get-level', action='store_true', help='Generate a level with a graph trained with --fit-to-agent')

graph_group = parser.add_mutually_exclusive_group(required=True)
graph_group.add_argument('--segment-graph', action='store_true', help='segment based generation for graph')
graph_group.add_argument('--n-gram-graph', action='store_true', help='n-gram based generation for graph')

rl_agent_group = parser.add_mutually_exclusive_group(required=True)
rl_agent_group.add_argument('--sarsa', action='store_true', help='SARSA Agent')
rl_agent_group.add_argument('--q', action='store_true', help='Q-Learning Agent')
rl_agent_group.add_argument('--policy', action='store_true', help='Policy Iteration Agent')
rl_agent_group.add_argument('--value', action='store_true', help='Value Iteration Agent')
rl_agent_group.add_argument('--online-value', action='store_true', help='Online Value Iteration Agent')
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
parser.add_argument('--gamma', type=float, default=0.75, help='Discount factor for all RL algorithms')
parser.add_argument('--runs', type=int, default=100, help='Number of runs for a person when --fit-person is used')
parser.add_argument('--playthroughs', type=int, default=20, help='Number of levels played per director')


args = parser.parse_args()

# Get Game 
if args.dungeongram:
    config = DungeonGrams
elif args.mario:
    config = Mario
elif args.icarus:
    config = Icarus

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
    graph = Utility.get_level_segment_graph(config, config.ALLOW_EMPTY_LINK)
    PLAYERS = SEGMENT_PLAYERS
else:
    graph, gram = Utility.get_n_gram_graph(config)
    PLAYERS = {
        'agent': GramPlayer(config).get
    }

    config.GRAM = gram

agents = []
if args.sarsa:
    agents.append(lambda: Directors.SARSA(deepcopy(graph), args.gamma))
if args.q or args.all:
    agents.append(lambda: Directors.QLearning(deepcopy(graph), args.gamma))
if args.policy or args.all:
    agents.append(lambda: Directors.PolicyIteration(deepcopy(graph), args.max_iter, args.policy_iter, args.gamma))
if args.online_value:
    agents.append(lambda: Directors.OnlineValueIteration(deepcopy(graph), args.gamma))
if args.value:
    agents.append(lambda: Directors.ValueIteration(deepcopy(graph), args.max_iter, args.gamma, args.theta))
if args.random or args.all:
    agents.append(lambda: Directors.Random(deepcopy(graph)))
if args.greedy or args.all:
    agents.append(lambda: Directors.Greedy(deepcopy(graph)))

# run task
if args.fit_agent:
    for rl_agent in agents:
        agent = rl_agent()
        print(f'Running Director: {agent.NAME}')
        seed(args.seed)
        task = FitAgent(agent, config, args.segments, args.playthroughs)
        data = task.run()

        # f_name = f'agent_game_{config.NAME}_director_{agent.NAME}_reward_{REWARD_StR}.pkl'
        # with open(join(config.BASE_DIR, f_name), 'wb') as f:
        #     pkl_dump(agent, f)

        # f_name =  f'fitagent_game_{config.NAME}_director_{agent.NAME}_reward_{REWARD_StR}.json'
        # with open(join(config.BASE_DIR, f_name), 'w') as f:
        #     json_dump(data, f, indent=2)

        print()
        print()

elif args.fit_persona:
    to_run = []
    for rl_agent in agents:
        for p_name, p_eval in PLAYERS.items():
            to_run.append((rl_agent, p_name, p_eval))
            
            name = rl_agent().NAME
            f_name = f'player_{p_name}_game_{config.NAME}_director_{name}_reward_{REWARD_StR}.json'
            path = join(config.BASE_DIR, f_name)
            if os.path.exists(path):
                os.remove(path)

    progress_bar = tqdm(to_run, leave=False)
    for rl_agent, p_name, p_eval in progress_bar:
        name = rl_agent().NAME # this is lazy but whatever
        progress_bar.set_description(f'{name} :: {p_name} :: {config.NAME}')
        data = []

        for i in trange(args.runs, leave=False):
            seed(args.seed+i)
            task = FitPlayerPersona(rl_agent(), config, args.segments, args.playthroughs, p_eval, args.n_gram_graph)
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
                'playthroughs': args.playthroughs
            }
        }

        f_name = f'player_{p_name}_game_{config.NAME}_director_{name}_reward_{REWARD_StR}.json'
        with open(join(config.BASE_DIR, f_name), 'w') as f:
            json_dump(res, f, indent=2)

elif args.switch_persona:
    for rl_agent in tqdm(agents, leave=False):
        data = []
        for i in trange(args.runs, leave=False):
            seed(args.seed+i)
            players = [
                bad_player_likes_easy_levels,
                good_player_likes_hard_levels,
            ]

            task = SwitchPlayerPersona(rl_agent(), config, args.segments, args.playthroughs, players, args.n_gram_graph)
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
                    'Bad Player Likes Easy Levels',
                    'Good Player Likes Hard Levels',
                ]
            }
        }

        f_name = f'switch_game_{config.NAME}_director_{rl_agent().NAME}_reward_{REWARD_StR}.json'
        with open(join(config.BASE_DIR, f_name), 'w') as f:
            json_dump(res, f, indent=2)

elif args.get_level:
    raise NotImplementedError('--get-level is not yet implemented')

end = time()

hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

# mac only
os.popen('say "Done!"')
print('Done!')