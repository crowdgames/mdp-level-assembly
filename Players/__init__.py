from random import random, uniform, choices

'''
All these functions return an array the size of the nodes array.

[
    "node_name",
    percent_compleatable [0,1],
    agent_enjoyment [0,1]
]
'''

def bad_player_likes_hard_levels(nodes, director):
    playthrough = []
    for n in nodes:
        cur_bc = sum(director.get_node_meta_data(n, 'bc'))
        if cur_bc < 0.5:
            # player beat the level but did not enjoy it
            playthrough.append([n, 1.0, 0.0]) 
        elif cur_bc < 0.75:
            # player beat the level, and kind of enjoyed it
            playthrough.append([n, 1.0, 0.1])
        elif random() > cur_bc / 2:
            # player beat the level, and enjoyed it relative to its difficulty
            playthrough.append([n, 1.0, cur_bc / 2])
        else:
            # player did not beat the whole level, but really enjoyed it
            playthrough.append([n, uniform(0.1, 0.9), 1.0])
            break

    return playthrough

def bad_player_likes_easy_levels(nodes, director):
    playthrough = []
    for n in nodes:
        cur_bc = sum(director.get_node_meta_data(n, 'bc'))
        if cur_bc < 0.1:
            # player beat the level but did not enjoy it
            playthrough.append([n, 1.0, 1.0]) 
        elif cur_bc < 0.5:
            # player beat the level, and kind of enjoyed it
            playthrough.append([n, 1.0, uniform(0.7, 0.9)])
        else:
            # player did not beat the whole level, but really enjoyed it
            playthrough.append([n, uniform(0.1, 0.3), uniform(0.01, 0.2)])
            break

    return playthrough

def good_player_likes_easy_levels(nodes, director):
    playthrough = []
    for n in nodes:
        cur_bc = sum(director.get_node_meta_data(n, 'bc'))
        if cur_bc < 0.1:
            # player beat the level but did not enjoy it
            playthrough.append([n, 1.0, 1.0]) 
        elif cur_bc < 0.5:
            # player beat the level, and kind of enjoyed it
            playthrough.append([n, 1.0, uniform(0.7, 0.9)])
        else:
            # player did not beat the whole level, but really enjoyed it
            playthrough.append([n, choices([1.9, uniform(0.6, 0.95)], weights=[0.9, 0.1])[0], uniform(0.01, 0.2)])
            break

    return playthrough

def mediocre_player_likes_high_a(nodes, director):
    raise NotImplementedError()

def mediocre_player_likes_high_b(nodes, director):
    raise NotImplementedError()

def mediocre_player_likes_hard_levels(nodes, director):
    raise NotImplementedError()

def mediocre_player_likes_easy_levels(nodes, direcotr):
    raise NotImplementedError()

PLAYERS = {
    'Bad Player Likes Hard Levels': bad_player_likes_hard_levels,
    'Bad Player Likes Easy Levels': bad_player_likes_easy_levels,
    'Good Player Likes Easy Levels': good_player_likes_easy_levels,
    # 'Mediocre Player Likes High A': mediocre_player_likes_high_a,
    # 'Mediocre Player Likes High B': mediocre_player_likes_high_b,
    # 'Mediocre Player likes Hard Levels': mediocre_player_likes_hard_levels,
    # 'Mediocre Player Likes Easy Levels': mediocre_player_likes_easy_levels
}