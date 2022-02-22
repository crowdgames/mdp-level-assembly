from email.policy import default
from Utility import Counter

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

    def __node_no_index(self, node):
        if '__' in node:
            return node
            
        a, b, _ = node.split(',')
        return f'{a},{b}'

    def run(self):
        cur = self.config.START_NODE
        data = []
        self.rl_agent.update([])
        counter = Counter()

        for i in range(50):
            lvl = []
            size = 1
            lvl += self.rl_agent.get_node_meta_data(cur, 'slices')
            nodes = [cur]
            lengths = [len(lvl)]
            while size < self.segments:
                # cur = self.rl_agent.weighted_neighbor(cur)
                # cur = self.rl_agent.best_neighbor(cur)
                cur = self.rl_agent.get(cur)
                counter.add(self.__node_no_index(cur))
                nodes.append(cur)
                segment = self.rl_agent.get_node_meta_data(cur, 'slices')
                lvl += segment
                lengths.append(len(segment))
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
            reward_always_one = True
            for node, r in playthrough:
                if '__' in node:
                    self.rl_agent.set_node_meta_data(
                        node, 
                        'r', 
                        self.rl_agent.get_node_meta_data(node, 'max_r') * r / counter.get(node, default=1))
                else:
                    a, b, _ = node.split(',')
                    index = 0
                    cur_node = f'{a},{b},{index}'
                    node_name = self.__node_no_index(cur_node)
                    while cur_node in self.rl_agent.G:
                        self.rl_agent.set_node_meta_data(
                            cur_node, 
                            'r', 
                            self.rl_agent.get_node_meta_data(node, 'max_r') * r / counter.get(node_name, default=1))
                        index +=1
                        cur_node = f'{a},{b},{index}'

                reward_always_one &= r==1.0
            
            # if not reward_always_one:
            #     from Utility import slices_to_rows
            #     print('Reward was not always one!')
            #     print()
            #     print()
            #     print(nodes)
            #     print(playthrough)
            #     for r in slices_to_rows(lvl, False):
            #         print(r)

            #     print()
            #     print()
            #     for n in nodes:
            #         print(n)
            #         for s in self.rl_agent.get_node_meta_data(n, 'slices'):
            #             print(s)
            #         print()
            #     import sys
            #     sys.exit(-1)

            cur = self.rl_agent.weighted_neighbor(cur)
            counter.add(cur)
            self.rl_agent.update(playthrough)
            print(f'{i}: {playthrough}')

        return data
   