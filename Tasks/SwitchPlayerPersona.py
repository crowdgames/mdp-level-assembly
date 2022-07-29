from .BaseFit import BaseFit

class SwitchPlayerPersona(BaseFit):
    def __init__(self, graph, director, config, segments, playthroughs, player_persona, need_full_level, hide_tqdm):
        super().__init__(graph, director, config, segments, playthroughs, not need_full_level, hide_tqdm)
        self.player_persona = player_persona
        self.need_full_level = need_full_level

    def run(self):
        data = []
        self._fit(data, self.player_persona[0], int(self.playthroughs*0.7))
        self._fit(data, self.player_persona[1], int(self.playthroughs*0.3))

        return data
   