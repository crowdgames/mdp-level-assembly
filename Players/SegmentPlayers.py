from GDM.Graph import Graph
from random import uniform
from typing import List

from .PlaythroughEntry import PlaythroughEntry
from .Playthrough import Playthrough

############ Bad Player
def bad_player_likes_hard_levels(G: Graph, nodes: List[str], MAX_BC: float) -> Playthrough:
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(G.get_node(n).behavioral_characteristics)
        agent_r = cur_bc / MAX_BC
        if cur_bc < MAX_BC * 0.25:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.1, 0.4), agent_r, 0.0, 0.0, 0.0))
            break

    return playthrough

def bad_player_likes_easy_levels(G: Graph, nodes: List[str], MAX_BC: float) -> Playthrough:
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(G.get_node(n).behavioral_characteristics)
        agent_r = (MAX_BC - cur_bc) / MAX_BC
        if cur_bc < MAX_BC*0.25:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.1, 0.4), agent_r, 0.0, 0.0, 0.0))
            break

    return playthrough

############ Good Player
def good_player_likes_easy_levels(G: Graph, nodes: List[str], MAX_BC: float) -> Playthrough:
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(G.get_node(n).behavioral_characteristics)
        agent_r = (MAX_BC - cur_bc) / MAX_BC

        if cur_bc < MAX_BC*0.75:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.6, 0.95), agent_r, 0.0, 0.0, 0.0))
            break

    return playthrough

def good_player_likes_hard_levels(G: Graph, nodes: List[str], MAX_BC: float) -> Playthrough:
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(G.get_node(n).behavioral_characteristics)
        agent_r = cur_bc / MAX_BC
        
        if cur_bc < MAX_BC*0.75:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.6, 0.95), agent_r, 0.0, 0.0, 0.0))
            break

    return playthrough

def mediocre_player_likes_high_a(G: Graph, nodes: List[str], MAX_BC: float) -> Playthrough:
    playthrough = Playthrough()
    for n in nodes:
        a,b = G.get_node(n).behavioral_characteristics
        cur_bc = a + b
        if cur_bc < MAX_BC * 0.5:
            playthrough.add(PlaythroughEntry(n, 1.0, a, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.4, 0.7), a, 0.0, 0.0, 0.0))
            break

    return playthrough

############ Mediocre Player
def mediocre_player_likes_high_b(G: Graph, nodes: List[str], MAX_BC: float) -> Playthrough:
    playthrough = Playthrough()

    for n in nodes:
        a,b = G.get_node(n).behavioral_characteristics
        cur_bc = a + b
        if cur_bc < MAX_BC * 0.5:
            playthrough.add(PlaythroughEntry(n, 1.0, b, 0.0, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.4, 0.7), b, 0.0, 0.0, 0.0))
            break

    return playthrough

def mediocre_player_likes_hard_levels(G: Graph, nodes: List[str], MAX_BC: float) -> Playthrough:
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(G.get_node(n).behavioral_characteristics)
        agent_r = cur_bc / MAX_BC

        if cur_bc < MAX_BC * 0.5:
            playthrough.add(PlaythroughEntry(n, 1.0, agent_r, 0.0, 0.0))
        else:
            playthrough.add(PlaythroughEntry(n, uniform(0.4, 0.7), agent_r, 0.0, 0.0))
            break

    return playthrough

def mediocre_player_likes_easy_levels(G: Graph, nodes: List[str], MAX_BC: float) -> Playthrough:
    playthrough = Playthrough()
    for n in nodes:
        cur_bc = sum(G.get_node(n).behavioral_characteristics)
        agent_r = (MAX_BC - cur_bc) / MAX_BC

        if cur_bc < MAX_BC*0.5:
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
#     'Good Player Likes Hard Levels': good_player_likes_hard_levels,
#     # 'Mediocre Player Likes High A': mediocre_player_likes_high_a,
#     # 'Mediocre Player Likes High B': mediocre_player_likes_high_b,
#     # 'Mediocre Player Likes Hard Levels': mediocre_player_likes_hard_levels,
#     # 'Mediocre Player Likes Easy Levels': mediocre_player_likes_easy_levels
# }