from .BaseFit import BaseFit

class FitPlayerPersona(BaseFit):
    def __init__(self, rl_agent, config, segments, playthroughs, player_persona):
        super().__init__(rl_agent, config, segments, playthroughs)
        self.player_persona = player_persona

    def run(self):
        cur = self.config.START_NODE
        data = []
        self.rl_agent.update([])

        for _ in range(self.playthroughs):
            _, nodes, __ = self.get_level(cur)
            cur = nodes[-1]

            playthrough = self.player_persona(nodes, self.rl_agent)
            data.append(playthrough)
            self.update_from_playthrough(playthrough) # reward added to playthrough here
            
            cur = self.rl_agent.weighted_neighbor(cur)
            self.counter.add(cur)
            self.rl_agent.update(playthrough)

        return data
   