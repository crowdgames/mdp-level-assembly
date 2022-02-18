from Tasks import *
from Games import *
import Utility
import Directors

from os.path import join
from random import seed
from time import time
from pickle import dump as pkl_dump
from json import dump as json_dump
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
task_group.add_argument('--fit-to-agent', action='store_true', help='Fit to an agent')
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

parser.add_argument('--segments', type=int, help='Number of segments to fit together', required=True)
parser.add_argument('--theta', type=float, default=1e-13, help='Convergence criteria for Ialue Iteration')
parser.add_argument('--max-iter', type=int, default=10_000, help='Max # of iterations for Value Iteration')
parser.add_argument('--policy-iter', type=int, default=20, help='# of iterations for Policy Evaluation step')
parser.add_argument('--gamma', type=float, default=0.75, help='Discount factor for all RL algorithms')
parser.add_argument('--empty-link', type=bool, default=True, help='Allow empty links')

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

graph = Utility.get_graph(config.BASE_DIR, config.TRANSPOSE, args.empty_link)
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
if args.fit_to_agent:
    for rl_agent in agents:
        print(f'Running agent: {rl_agent.NAME}')
        seed(args.seed)
        task = FitAgent(rl_agent, config, args.segments)
        data = task.run()

        with open(join(config.BASE_DIR, f'agent_{config.NAME}_{rl_agent.NAME}.pkl'), 'wb') as f:
            pkl_dump(rl_agent, f)

        with open(join(config.BASE_DIR, f'fitagent_playthrough_{config.NAME}_{rl_agent.NAME}.json'), 'w') as f:
            json_dump(data, f, indent=2)
        print()
        print()
        
elif args.get_level:
    raise NotImplementedError('--get-level is not yet implemented')

end = time()

hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

# mac only
os.popen('say "Done!"')