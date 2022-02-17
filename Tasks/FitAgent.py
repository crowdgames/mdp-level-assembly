from json import dump

from Utility.util import slices_to_rows

class FitAgent:
    def __init__(self, rl_agent, config, segments):
        self.rl_agent = rl_agent
        self.config = config
        self.segments = segments
        
        if config.WRAPS:
            self.get_playthrough = self.__playthrough_on_y
        else:
            self.get_playthrough = self.__playthrough_on_x

    def __playthrough_on_x(self, x, y, nodes, lengths):
        playthrough = []
        for n, l in zip(nodes, lengths):
            new_x = x - l
            if new_x > 0:
                playthrough.append((n, 1.0))
                x = new_x
            else:
                playthrough.append((n, x / l))
                break

        return playthrough

    def __playthrough_on_y(self, x, y, nodes, lengths):
        playthrough = []
        for n, l in zip(nodes, lengths):
            new_y = y - l
            if y > 0:
                playthrough.append((n, 1.0))
                y = new_y
            else:
                playthrough.append((n, y / l))
                break

        return playthrough

    def run(self):
        cur = '0,0,0'
        data = []
        for i in range(18):
            lvl = []
            size = 1
            lvl += self.rl_agent.get_node_meta_data(cur, 'slices')
            nodes = [cur]
            lengths = [len(lvl)]
            while size < self.segments:
                cur = self.rl_agent.weighted_neighbor(cur)
                # cur = self.rl_agent.best_neighbor(cur)
                nodes.append(cur)
                lvl += self.rl_agent.get_node_meta_data(cur, 'slices')
                lengths.append(len(self.rl_agent.get_node_meta_data(cur, 'slices')))
                size += 1 * '__' not in cur # small optimization to remove branching

            lengths[0] += self.config.PADDING_SIZE 
            lengths[-1] += self.config.PADDING_SIZE

            x, y = self.config.get_furthest_xy(lvl)
            
            playthrough = self.get_playthrough(
                x*len(lvl)+self.config.PADDING_SIZE*2, 
                y*len(lvl[0])+self.config.PADDING_SIZE*2, 
                nodes, 
                lengths)

            data.append(playthrough)
            for node, r in playthrough:
                self.rl_agent.set_node_meta_data(
                    node, 
                    'r', 
                    self.rl_agent.get_node_meta_data(node, 'max_r') * r)

            cur = self.rl_agent.weighted_neighbor(cur)
            self.rl_agent.update(playthrough)
            print(f'{i}: {playthrough}')

        return data
   