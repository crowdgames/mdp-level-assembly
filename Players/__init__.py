from random import random, uniform

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



PLAYERS = {
    'Bad Player Likes Hard Levels': bad_player_likes_hard_levels
}