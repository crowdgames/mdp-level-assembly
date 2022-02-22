from .BaseFit import BaseFit

class FitAgent(BaseFit):
    def __init__(self, rl_agent, config, segments):
        super().__init__(rl_agent, config, segments)

        if config.WRAPS:
            self.get_playthrough = self.__playthrough_on_y
        else:
            self.get_playthrough = self.__playthrough_on_x

    def __playthrough_on_x(self, x, y, nodes, lengths):
        playthrough = []
        for n, l in zip(nodes, lengths):
            new_x = x - l
            if new_x > 0:
                playthrough.append([n, 1.0])
                x = new_x
            else:
                playthrough.append([n, x / l])
                break

        return playthrough

    def __playthrough_on_y(self, x, y, nodes, lengths):
        playthrough = []
        for n, l in zip(nodes, lengths):
            new_y = y - l
            if y > 0:
                playthrough.append([n, 1.0])
                y = new_y
            else:
                playthrough.append([n, y / l])
                break

        return playthrough

    def run(self):
        cur = self.config.START_NODE
        data = []
        self.rl_agent.update([])

        for i in range(50):
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
            
            cur = self.rl_agent.weighted_neighbor(cur)
            self.counter.add(cur)
            self.rl_agent.update(playthrough)
            print(f'{i}: {playthrough}')

        return data
   