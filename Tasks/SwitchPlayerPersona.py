from .BaseFit import BaseFit

class SwitchPlayerPersona(BaseFit):
    def __init__(self, rl_agent, config, segments, playthroughs, player_persona, need_full_level):
        super().__init__(rl_agent, config, segments, playthroughs, not need_full_level)
        self.player_persona = player_persona
        self.need_full_level = need_full_level

    def run(self):
        cur = self.config.START_NODE
        data = []

        self.rl_agent.update(None)
        cur = self._fit(cur, data, self.player_persona[0], int(self.playthroughs*0.7))
        self._fit(cur, data, self.player_persona[1], int(self.playthroughs*0.3))

        return data
   