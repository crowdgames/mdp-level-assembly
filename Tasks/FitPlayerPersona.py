from .BaseFit import BaseFit

class FitPlayerPersona(BaseFit):
    def __init__(self, rl_agent, config, segments):
        super.__init__(rl_agent, config, segments)

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
            reward_always_one = True
            for entry in playthrough:
                node, r = entry
                if '__' in node:
                    self.rl_agent.set_node_meta_data(
                        node, 
                        'r', 
                        self.rl_agent.get_node_meta_data(node, 'max_r') * r / self.counter.get(node, default=1))
                else:
                    a, b, _ = node.split(',')
                    index = 0
                    cur_node = f'{a},{b},{index}'
                    node_name = self.__node_no_index(cur_node)
                    while cur_node in self.rl_agent.G:
                        self.rl_agent.set_node_meta_data(
                            cur_node, 
                            'r', 
                            self.rl_agent.get_node_meta_data(node, 'max_r') * r / self.counter.get(node_name, default=1))
                        index +=1
                        cur_node = f'{a},{b},{index}'

                entry.append(self.rl_agent.get_node_meta_data(node, 'r'))
                reward_always_one &= r==1.0
            

            cur = self.rl_agent.weighted_neighbor(cur)
            self.counter.add(cur)
            self.rl_agent.update(playthrough)
            print(f'{i}: {playthrough}')

        return data
   