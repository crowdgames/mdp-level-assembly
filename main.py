from Tasks import *
from Games import *
from Players import PLAYERS
from Tasks.FitPlayerPersona import FitPlayerPersona
import Utility
import Directors

from os.path import join
from random import seed
from time import time
from pickle import dump as pkl_dump
from json import dump as json_dump
from tqdm import trange
import argparse
import sys
import os

start = time()

parser = argparse.ArgumentParser(description='Graph Procedural Content Generation via Reinforcement Learning')
parser.add_argument('--seed', type=int, default=0, help='Set seed for generation')

game_group = parser.add_mutually_exclusive_group(required=True)
game_group.add_argument('--dungeongram', action='store_true', help='Run DungeonGrams')
game_group.add_argument('--dungeongram-food', action='store_true', help='Run DungeonGrams with required food linkers')
game_group.add_argument('--mario', action='store_true', help='Run Mario')
game_group.add_argument('--icarus', action='store_true', help='Run Icarus')

task_group = parser.add_mutually_exclusive_group(required=True)
task_group.add_argument('--fit-agent', action='store_true', help='Fit to an agent')
task_group.add_argument('--fit-persona', action='store_true', help='Fit to a player persona')
task_group.add_argument('--get-level', action='store_true', help='Generate a level with a graph trained with --fit-to-agent')

rl_agent_group = parser.add_mutually_exclusive_group(required=True)
rl_agent_group.add_argument('--sarsa', action='store_true', help='SARSA agent')
rl_agent_group.add_argument('--q', action='store_true', help='Q-Learning agent')
rl_agent_group.add_argument('--policy', action='store_true', help='Policy Iteration agent')
rl_agent_group.add_argument('--value', action='store_true', help='Value Iteration agent')
rl_agent_group.add_argument('--random', action='store_true', help='Randomly choose where to go regardless of the player')
rl_agent_group.add_argument('--greedy-max', action='store_true', help='Greedily choose where to go based on the max reward')
rl_agent_group.add_argument('--greedy-relative', action='store_true', help='Greedily choose where to go based on the reward')
rl_agent_group.add_argument('--all', action='store_true', help='Run every agent')

parser.add_argument('--segments', type=int, default=3, help='Number of segments to fit together')
parser.add_argument('--theta', type=float, default=1e-13, help='Convergence criteria for Ialue Iteration')
parser.add_argument('--max-iter', type=int, default=100, help='Max # of iterations for Value Iteration')
parser.add_argument('--policy-iter', type=int, default=20, help='# of iterations for Policy Evaluation step')
parser.add_argument('--gamma', type=float, default=0.75, help='Discount factor for all RL algorithms')
parser.add_argument('--empty-link', type=bool, default=True, help='Allow empty links')
parser.add_argument('--runs', type=int, default=100, help='Number of runs for a person when --fit-person is used')
parser.add_argument('--playthroughs', type=int, default=50, help='Number of levels played per director')


args = parser.parse_args()

# Get Game 
if args.dungeongram:
    config = DungeonGrams
    assert 'Dungeon Grams is not yet supported'
elif args.dungeongram_food:
    config = DungeonGrams
    assert 'Dungeon Grams is not yet supported'
    assert 'No support for dungeongrams with food linkers yet'
elif args.mario:
    config = Mario
elif args.icarus:
    config = Icarus

graph = Utility.get_graph(config, args.empty_link)
agents = []
if args.sarsa or args.all:
    agents.append(Directors.SARSA(graph, args.gamma))
if args.q or args.all:
    agents.append(Directors.QLearning(graph, args.gamma))
if args.policy or args.all:
    agents.append(Directors.PolicyIteration(graph, args.max_iter, args.policy_iter, args.gamma))
if args.value or args.all:
    agents.append(Directors.ValueIteration(graph, args.max_iter, args.gamma, args.theta))
if args.random or args.all:
    agents.append(Directors.Random(graph))
if args.greedy_max or args.all:
    agents.append(Directors.GreedyMax(graph))
if args.greedy_relative or args.all:
    agents.append(Directors.GreedyRelative(graph))

# run task
if args.fit_agent:
    for rl_agent in agents:
        print(f'Running Director: {rl_agent.NAME}')
        seed(args.seed)
        task = FitAgent(rl_agent, config, args.segments, args.playthroughs)
        data = task.run()

        with open(join(config.BASE_DIR, f'agent_{config.NAME}_{rl_agent.NAME}.pkl'), 'wb') as f:
            pkl_dump(rl_agent, f)

        with open(join(config.BASE_DIR, f'fitagent_playthrough_{config.NAME}_{rl_agent.NAME}.json'), 'w') as f:
            json_dump(data, f, indent=2)

        print()
        print()

elif args.fit_persona:
    for rl_agent in agents:
        seed(args.seed)
        for PLAYER_NAME, PLAYER_EVAL in PLAYERS.items():
            print(f'Running Director: {rl_agent.NAME} for player {PLAYER_NAME}')
            data = []
            for i in trange(args.runs):
                seed(args.seed+i)
                task = FitPlayerPersona(rl_agent, config, args.segments, args.playthroughs, PLAYER_EVAL)
                data.append(task.run())

            with open(join(config.BASE_DIR, f'player_{PLAYER_NAME}_fit_playthrough_{config.NAME}_{rl_agent.NAME}.json'), 'w') as f:
                json_dump(data, f, indent=2)

elif args.get_level:
    raise NotImplementedError('--get-level is not yet implemented')

end = time()

hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

# mac only
os.popen('say "Done!"')