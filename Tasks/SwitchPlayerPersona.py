from .BaseFit import BaseFit
from tqdm import trange

class SwitchPlayerPersona(BaseFit):
    def __init__(self, rl_agent, config, segments, playthroughs, player_persona, need_full_level):
        super().__init__(rl_agent, config, segments, playthroughs, not need_full_level)
        self.player_persona = player_persona
        self.need_full_level = need_full_level

    def __fit(self, cur, data, player_persona, num_playthroughs):
        for _ in trange(num_playthroughs, leave=False):
            if self.need_full_level:
                # an agent is going to play the game
                lvl, nodes, lengths = self.get_level(cur)
                playthrough = player_persona(lvl, nodes, lengths)
                assert self.config.GRAM.sequence_is_possible(lvl)
            else:
                # surrogate is going to play it
                nodes = self.get_level_nodes(cur)
                playthrough = player_persona(nodes, self.rl_agent, self.config.NUM_BC)

            self.update_from_playthrough(playthrough) # reward added to playthrough here
            
            # rl agent learns from the playthrough and selects where to start from next time.
            # important to note that this is based on where the player was at last and not
            # the last node that they could have visited.
            self.rl_agent.update(playthrough)
            cur = self.rl_agent.get(playthrough.entries[-1].node_name)

            # make sure the node in question is not a link. If it is then go to the 
            # next node.
            if '__' in cur:
                cur = cur.split('__')[1]

            # output data is updated 
            data.append(playthrough.get_summary(nodes))

        return cur

    def run(self):
        cur = self.config.START_NODE
        data = []

        self.rl_agent.update(None)
        cur = self.__fit(cur, data, self.player_persona[0], int(self.playthroughs*0.7))
        self.__fit(cur, data, self.player_persona[1], int(self.playthroughs*0.3))

        return data
   