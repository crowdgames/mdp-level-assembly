from .BaseFit import BaseFit
from Players import Playthrough, PlaythroughEntry

class FitAgent(BaseFit):
    def __init__(self, director, config, segments, playthroughs):
        super().__init__(director, config, segments, playthroughs)

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
                playthrough.add(PlaythroughEntry(n, x/l, 0.0))
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
                playthrough.add(PlaythroughEntry(n, y/l, 0.0))
                break

        return playthrough

    def run(self):
        cur = self.config.START_NODE
        data = []
        self.director.update(None)

        for i in range(self.playthroughs):
            lvl, nodes, lengths = self.get_level(cur)
            cur = nodes[-1]

            x, y = self.config.get_furthest_xy(lvl)
            playthrough = self.get_playthrough(
                x*len(lvl)+self.config.PADDING_SIZE*2, 
                y*len(lvl[0])+self.config.PADDING_SIZE*2, 
                nodes, 
                lengths)

            data.append(playthrough)
            self.update_from_playthrough(playthrough)
            
            # make sure the node in question is not a link. If it is then go to the 
            # next node.
            cur = self.director.get(cur)
            if '__' in cur:
                cur = cur.split('__')[1]

            self.director.update(playthrough)
            print(f'{i}: {playthrough.get_summary(nodes)}')

        return data
   