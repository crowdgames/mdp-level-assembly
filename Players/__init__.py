from random import random, uniform

'''
All these functions return an array the size of the nodes array.

[
    "node_name",
    percent_compleatable [0,1],
    agent_enjoyment [0,1]
]
'''

def bad_player_likes_hard_levels(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        cur_bc = sum(director.get_node_meta_data(n, 'bc'))
        agent_r = cur_bc / MAX_BC
        if cur_bc < MAX_BC*0.3 or random() > cur_bc/ MAX_BC:
            playthrough.append([n, 1.0, agent_r])
        else:
            playthrough.append([n, uniform(0.1, 0.9), agent_r])
            break

    return playthrough

def bad_player_likes_easy_levels(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        cur_bc = sum(director.get_node_meta_data(n, 'bc'))
        agent_r = (MAX_BC - cur_bc) / MAX_BC
        if cur_bc < MAX_BC*0.3 or random() > cur_bc / MAX_BC:
            playthrough.append([n, 1.0, agent_r]) 
        else:
            playthrough.append([n, uniform(0.1, 0.3), agent_r])
            break

    return playthrough

def good_player_likes_easy_levels(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        cur_bc = sum(director.get_node_meta_data(n, 'bc'))
        agent_r = (MAX_BC - cur_bc) / MAX_BC
        
        if cur_bc < MAX_BC*0.7 or random() > cur_bc / MAX_BC:
            playthrough.append([n, 1.0, agent_r]) 
        else:
            playthrough.append([n, uniform(0.1, 0.8), agent_r])
            break

    return playthrough

def mediocre_player_likes_high_a(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        a, b = director.get_node_meta_data(n, 'bc')
        cur_bc = a + b
        if cur_bc < MAX_BC * 0.5 or random() > cur_bc / MAX_BC:
            playthrough.append([n, 1.0, a]) 
        else:
            playthrough.append([n, uniform(0.5, 1.0), a])
            break

    return playthrough

def mediocre_player_likes_high_b(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        a, b = director.get_node_meta_data(n, 'bc')
        cur_bc = a + b
        if cur_bc < MAX_BC*0.4 or random() > cur_bc / MAX_BC:
            playthrough.append([n, 1.0, b]) 
        else:
            playthrough.append([n, uniform(0.5, 1.0), b])
            break

    return playthrough

def mediocre_player_likes_hard_levels(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        cur_bc = sum(director.get_node_meta_data(n, 'bc'))
        agent_r = cur_bc / MAX_BC

        if cur_bc < MAX_BC*0.4 or random() > cur_bc / MAX_BC:
            playthrough.append([n, 1.0, agent_r]) 
        else:
            playthrough.append([n, uniform(0.5, 1.0), agent_r])
            break

    return playthrough

def mediocre_player_likes_easy_levels(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        cur_bc = sum(director.get_node_meta_data(n, 'bc'))
        agent_r = (MAX_BC - cur_bc) / MAX_BC

        if cur_bc < MAX_BC*0.4 or random() > cur_bc / MAX_BC:
            playthrough.append([n, 1.0, agent_r]) 
        else:
            playthrough.append([n, uniform(0.5, 1.0), agent_r])
            break

    return playthrough

PLAYERS = {
    'Bad Player Likes Hard Levels': bad_player_likes_hard_levels,
    'Bad Player Likes Easy Levels': bad_player_likes_easy_levels,
    'Good Player Likes Easy Levels': good_player_likes_easy_levels,
    'Mediocre Player Likes High A': mediocre_player_likes_high_a,
    'Mediocre Player Likes High B': mediocre_player_likes_high_b,
    'Mediocre Player likes Hard Levels': mediocre_player_likes_hard_levels,
    'Mediocre Player Likes Easy Levels': mediocre_player_likes_easy_levels
}