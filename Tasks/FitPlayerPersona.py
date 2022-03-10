from .BaseFit import BaseFit
from tqdm import trange
from Players import build_summary

class FitPlayerPersona(BaseFit):
    def __init__(self, rl_agent, config, segments, playthroughs, player_persona):
        super().__init__(rl_agent, config, segments, playthroughs)
        self.player_persona = player_persona

    def run(self):
        cur = self.config.START_NODE
        data = []
        self.rl_agent.update([])

        for _ in trange(self.playthroughs, leave=False):
            # build the level and let the player play through it
            nodes = self.get_level_nodes(cur)
            playthrough = self.player_persona(nodes, self.rl_agent, self.config.NUM_BC)
            self.update_from_playthrough(playthrough) # reward added to playthrough here
            
            # rl agent learns from the playthrough and selects where to start from next time.
            self.rl_agent.update(playthrough)
            cur = self.rl_agent.weighted_neighbor(nodes[-1])
            self.counter.add(cur)

            # output data is updated 
            data.append(build_summary(nodes, playthrough))

        return data
   