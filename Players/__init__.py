from random import random, uniform
from Directors.Keys import *

NAME = 'node_name'
PC = 'Percent Completable'
AR = 'Agent Reward'
DR = 'Designer Reward'
TR = 'Total Reward'

class PlaythroughEntry:
    def __init__(self, node, percent_completable, player_reward):
        self.node_name = node
        self.percent_completable = percent_completable
        self.player_reward = player_reward
        self.designer_reward = 0  # this is set later in the process
        self.total_reward = 0     # this is set later in the process

    def to_dict(self):
        return {
            NAME: self.node_name,
            PC: self.percent_completable,
            AR: self.player_reward,
            DR: self.designer_reward,
            TR: self.total_reward
        }

class Playthrough:
    def __init__(self):
        self.entries = []

    def add(self, playthrough_entry):
        self.entries.append(playthrough_entry)

    def get_summary(self, nodes):
        percent_complete = 0
        percent_player_reward = 0
        percent_design_reward = 0
        percent_total_reward = 0

        for entry in self.entries:
            percent_complete += entry.percent_completable
            percent_player_reward += entry.player_reward
            percent_design_reward += entry.designer_reward
            percent_total_reward += entry.total_reward

        # percent_complete is based on how far the player should have been able to go.
        # The other two are based on what the player experienced.
        percent_complete /= len(nodes)
        percent_player_reward /= len(self.entries)
        percent_design_reward /= len(self.entries)
        percent_total_reward /= len(self.entries)

        return {
            'Playthrough': [e.to_dict() for e in self.entries],
            'percent_complete': percent_complete,
            'percent_player_reward': percent_player_reward,
            'percent_design_reward': percent_design_reward,
            'percent_total_reward': percent_total_reward,
        }

def bad_player_likes_hard_levels(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(director.get_md(n, BC))
        agent_r = cur_bc / MAX_BC
        if cur_bc < MAX_BC * 0.2:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.1, 0.9), agent_r))
            break

    return playthrough

def bad_player_likes_easy_levels(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(director.get_md(n, BC))
        agent_r = (MAX_BC - cur_bc) / MAX_BC
        if cur_bc < MAX_BC*0.2:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.1, 0.3), agent_r))
            break

    return playthrough

def good_player_likes_easy_levels(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(director.get_md(n, BC))
        agent_r = (MAX_BC - cur_bc) / MAX_BC

        if cur_bc < MAX_BC*0.8:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.6, 0.95), agent_r))
            break

    return playthrough

def good_player_likes_hard_levels(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(director.get_md(n, BC))
        agent_r = cur_bc / MAX_BC
        
        if cur_bc < MAX_BC*0.8:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.6, 0.95), agent_r))
            break

    return playthrough

def mediocre_player_likes_high_a(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        a, b = director.get_md(n, BC)
        cur_bc = a + b
        if cur_bc < MAX_BC * 0.5:
            playthrough.add(PlaythroughEntry(n, 1.0, a))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.4, 0.7), a))
            break

    return playthrough

def mediocre_player_likes_high_b(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        a, b = director.get_md(n, BC)
        cur_bc = a + b
        if cur_bc < MAX_BC * 0.5:
            playthrough.add(PlaythroughEntry(n, 1.0, b))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.4, 0.7), b))
            break

    return playthrough

def mediocre_player_likes_hard_levels(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(director.get_md(n, BC))
        agent_r = cur_bc / MAX_BC

        if cur_bc < MAX_BC * 0.5:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.4, 0.7), agent_r))
            break

    return playthrough

def mediocre_player_likes_easy_levels(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(director.get_md(n, BC))
        agent_r = (MAX_BC - cur_bc) / MAX_BC

        if cur_bc < MAX_BC*0.4:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.4, 0.7), agent_r))
            break

    return playthrough

PLAYERS = {
    'Bad Player Likes Hard Levels': bad_player_likes_hard_levels,
    'Bad Player Likes Easy Levels': bad_player_likes_easy_levels,
    # 'Good Player Likes Easy Levels': good_player_likes_easy_levels,
    # 'Good Player Likes Hard Levels': good_player_likes_hard_levels,
    # 'Mediocre Player Likes High A': mediocre_player_likes_high_a,
    # 'Mediocre Player Likes High B': mediocre_player_likes_high_b,
    # 'Mediocre Player Likes Hard Levels': mediocre_player_likes_hard_levels,
    # 'Mediocre Player Likes Easy Levels': mediocre_player_likes_easy_levels
}