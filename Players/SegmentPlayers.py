from random import uniform
from Directors.Keys import *

from .Playthrough import Playthrough
from .PlaythroughEntry import PlaythroughEntry

def bad_player_likes_hard_levels(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(director.get_md(n, BC))
        agent_r = cur_bc / MAX_BC
        if cur_bc < MAX_BC * 0.15:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.1, 0.9), agent_r, 0.0, 0.0, 0.0))
            break

    return playthrough

def bad_player_likes_easy_levels(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(director.get_md(n, BC))
        agent_r = (MAX_BC - cur_bc) / MAX_BC
        if cur_bc < MAX_BC*0.15:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.1, 0.3), agent_r, 0.0, 0.0, 0.0))
            break

    return playthrough

def good_player_likes_easy_levels(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(director.get_md(n, BC))
        agent_r = (MAX_BC - cur_bc) / MAX_BC

        if cur_bc < MAX_BC*0.8:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.6, 0.95), agent_r, 0.0, 0.0, 0.0))
            break

    return playthrough

def good_player_likes_hard_levels(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(director.get_md(n, BC))
        agent_r = cur_bc / MAX_BC
        
        if cur_bc < MAX_BC*0.8:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.6, 0.95), agent_r, 0.0, 0.0, 0.0))
            break

    return playthrough

def mediocre_player_likes_high_a(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        a, b = director.get_md(n, BC)
        cur_bc = a + b
        if cur_bc < MAX_BC * 0.3:
            playthrough.add(PlaythroughEntry(n, 1.0, a, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.4, 0.7), a, 0.0, 0.0, 0.0))
            break

    return playthrough

def mediocre_player_likes_high_b(nodes, director, MAX_BC):
    playthrough = Playthrough()

    for n in nodes:
        a, b = director.get_md(n, BC)
        cur_bc = a + b
        if cur_bc < MAX_BC * 0.3:
            playthrough.add(PlaythroughEntry(n, 1.0, b, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.4, 0.7), b, 0.0, 0.0, 0.0))
            break

    return playthrough

def mediocre_player_likes_hard_levels(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(director.get_md(n, BC))
        agent_r = cur_bc / MAX_BC

        if cur_bc < MAX_BC * 0.35:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.4, 0.7), agent_r, 0.0, 0.0))
            break

    return playthrough

def mediocre_player_likes_easy_levels(nodes, director, MAX_BC):
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(director.get_md(n, BC))
        agent_r = (MAX_BC - cur_bc) / MAX_BC

        if cur_bc < MAX_BC*0.35:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.4, 0.7), agent_r, 0.0, 0.0, 0.0))
            break

    return playthrough

PLAYERS = {
    'Bad Player Likes Hard Levels': bad_player_likes_hard_levels,
    # 'Bad Player Likes Easy Levels': bad_player_likes_easy_levels,
    'Good Player Likes Easy Levels': good_player_likes_easy_levels,
    'Good Player Likes Hard Levels': good_player_likes_hard_levels,
    'Mediocre Player Likes High A': mediocre_player_likes_high_a,
    'Mediocre Player Likes High B': mediocre_player_likes_high_b,
    # 'Mediocre Player Likes Hard Levels': mediocre_player_likes_hard_levels,
    # 'Mediocre Player Likes Easy Levels': mediocre_player_likes_easy_levels
}

# PLAYERS = {
#     # 'Bad Player Likes Hard Levels': bad_player_likes_hard_levels,
#     # 'Bad Player Likes Easy Levels': bad_player_likes_easy_levels,
#     # 'Good Player Likes Easy Levels': good_player_likes_easy_levels,
#     # 'Good Player Likes Hard Levels': good_player_likes_hard_levels,
#     'Mediocre Player Likes High A': mediocre_player_likes_high_a,
#     'Mediocre Player Likes High B': mediocre_player_likes_high_b,
#     # 'Mediocre Player Likes Hard Levels': mediocre_player_likes_hard_levels,
#     # 'Mediocre Player Likes Easy Levels': mediocre_player_likes_easy_levels
# }