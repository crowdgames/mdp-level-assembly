from .PlaythroughEntry import PlaythroughEntry
from .Playthrough import Playthrough

class GramPlayer:
    def __init__(self, config):
        self.config = config

        if config.WRAPS:
            self.get_playthrough = self.__playthrough_on_y
        else:
            self.get_playthrough = self.__playthrough_on_x

    def __playthrough_on_x(self, x, y, nodes):
        playthrough =  Playthrough()

        cur_x = self.config.PADDING_SIZE
        for n in nodes:
            if cur_x < x:
                playthrough.add(PlaythroughEntry(n, 1.0, 0.0, 0.0, 0.0, 0.0))
            else:
                playthrough.add(PlaythroughEntry(n, cur_x/len(nodes), 0.0, 0.0, 0.0, 0.0))
                break

            cur_x += 1
        
        return playthrough

    def __playthrough_on_y(self, x, y, nodes):
        raise NotImplementedError('Copy basically what x is')
        # playthrough =  Playthrough()

        # cur_x = self.config.PADDING_SIZE
        # for n in nodes:
        #     if cur_x < x:
        #         playthrough.add(PlaythroughEntry(n, 1.0, 0.0, 0.0, 0.0, 0.0))
                
        #     else:
        #         playthrough.add(PlaythroughEntry(n, 0.0, 0.0, 0.0, 0.0, 0.0))
        #         break
        
        # return playthrough

    def get(self, lvl, nodes, _):
        x, y = self.config.get_furthest_xy(self.config, lvl)
        playthrough = self.get_playthrough(x, y, nodes)

        for slice, entry in zip(lvl, playthrough.entries):
            entry.player_reward = self.config.player_reward(slice)

        return playthrough

