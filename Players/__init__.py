from random import random, uniform

'''
All these functions return an array the size of the nodes array.

[
    "node_name",
    percent_compleatable [0,1],
    agent_enjoyment [0,1]
]
'''

def build_summary(nodes, playthrough):
    percent_complete = 0
    percent_player_reward = 0
    percent_design_reward = 0
    percent_total_reward = 0

    for _, pc, ae, dr, r in playthrough:
        percent_complete += pc
        percent_player_reward += ae
        percent_design_reward += dr
        percent_total_reward += r

    # percent_complete is based on how far the player should have been able to go.
    # The other two are based on what the player experienced.
    percent_complete /= len(nodes)
    percent_player_reward /= len(playthrough)
    percent_design_reward /= len(playthrough)
    percent_total_reward /= len(playthrough)

    return {
        'playthrough': playthrough,
        'percent_complete': percent_complete,
        'percent_player_reward': percent_player_reward,
        'percent_design_reward': percent_design_reward,
        'percent_total_reward': percent_total_reward,
    }

def bad_player_likes_hard_levels(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        cur_bc = sum(director.get_node_meta_data(n, 'bc'))
        agent_r = cur_bc / MAX_BC
        if cur_bc < MAX_BC * 0.2:
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
        if cur_bc < MAX_BC*0.2:
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

        if cur_bc < MAX_BC*0.8:
            playthrough.append([n, 1.0, agent_r]) 
        else:
            playthrough.append([n, uniform(0.6, 0.95), agent_r])
            break

    return playthrough

def good_player_likes_hard_levels(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        cur_bc = sum(director.get_node_meta_data(n, 'bc'))
        agent_r = cur_bc / MAX_BC
        
        if cur_bc < MAX_BC*0.8:
            playthrough.append([n, 1.0, agent_r]) 
        else:
            playthrough.append([n, uniform(0.6, 0.95), agent_r])
            break

    return playthrough

def mediocre_player_likes_high_a(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        a, b = director.get_node_meta_data(n, 'bc')
        cur_bc = a + b
        if cur_bc < MAX_BC * 0.5:
            playthrough.append([n, 1.0, a]) 
        else:
            playthrough.append([n, uniform(0.4, 0.7), a])
            break

    return playthrough

def mediocre_player_likes_high_b(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        a, b = director.get_node_meta_data(n, 'bc')
        cur_bc = a + b
        if cur_bc < MAX_BC * 0.5:
            playthrough.append([n, 1.0, b]) 
        else:
            playthrough.append([n, uniform(0.4, 0.7), b])
            break

    return playthrough

def mediocre_player_likes_hard_levels(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        cur_bc = sum(director.get_node_meta_data(n, 'bc'))
        agent_r = cur_bc / MAX_BC

        if cur_bc < MAX_BC * 0.5:
            playthrough.append([n, 1.0, agent_r]) 
        else:
            playthrough.append([n, uniform(0.4, 0.7), agent_r])
            break

    return playthrough

def mediocre_player_likes_easy_levels(nodes, director, MAX_BC):
    playthrough = []
    for n in nodes:
        cur_bc = sum(director.get_node_meta_data(n, 'bc'))
        agent_r = (MAX_BC - cur_bc) / MAX_BC

        if cur_bc < MAX_BC*0.4:
            playthrough.append([n, 1.0, agent_r]) 
        else:
            playthrough.append([n, uniform(0.4, 0.7), agent_r])
            break

    return playthrough

PLAYERS = {
    'Bad Player Likes Hard Levels': bad_player_likes_hard_levels,
    'Bad Player Likes Easy Levels': bad_player_likes_easy_levels,
    'Good Player Likes Easy Levels': good_player_likes_easy_levels,
    'Good Player Likes Hard Levels': good_player_likes_hard_levels,
    'Mediocre Player Likes High A': mediocre_player_likes_high_a,
    'Mediocre Player Likes High B': mediocre_player_likes_high_b,
    'Mediocre Player Likes Hard Levels': mediocre_player_likes_hard_levels,
    'Mediocre Player Likes Easy Levels': mediocre_player_likes_easy_levels
}