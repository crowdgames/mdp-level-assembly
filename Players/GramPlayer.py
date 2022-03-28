from .PlaythroughEntry import PlaythroughEntry
from .Playthrough import Playthrough

class GramPlayer:
    def __init__(self, config):
        self.config = config

        if config.WRAPS:
            self.get_playthrough = self.__playthrough_on_y
        else:
            self.get_playthrough = self.__playthrough_on_x

    def __playthrough_on_x(self, x, y, nodes, lengths):
        playthrough = Playthrough()
        for n, l in zip(nodes, lengths):
            new_x = x - l
            if new_x > 0:
                playthrough.add(PlaythroughEntry(n, 1.0, 0.0))
                x = new_x
            else:
                playthrough.add(PlaythroughEntry(n, 0.0, 0.0))
                break

        return playthrough

    def __playthrough_on_y(self, x, y, nodes, lengths):
        playthrough =  Playthrough()
        for n, l in zip(nodes, lengths):
            new_y = y - l
            if y > 0:
                playthrough.add(PlaythroughEntry(n, 1.0, 0.0))
                y = new_y
            else:
                playthrough.add(PlaythroughEntry(n, 0.0, 0.0))
                break
        
        return playthrough

    def get(self, lvl, nodes, lengths):
        x, y = self.config.get_furthest_xy(lvl)
        playthrough = self.get_playthrough(
            x*len(lvl)+self.config.PADDING_SIZE*2, 
            y*len(lvl[0])+self.config.PADDING_SIZE*2, 
            nodes, 
            lengths)

        for slice, entry in zip(lvl, playthrough.entries):
            entry.player_reward = self.config.player_reward(slice)

        return playthrough

