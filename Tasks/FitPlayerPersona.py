from .BaseFit import BaseFit

class FitPlayerPersona(BaseFit):
    def __init__(self, director, config, segments, playthroughs, player_persona, need_full_level, hide_tqdm):
        super().__init__(director, config, segments, playthroughs, not need_full_level, hide_tqdm)
        self.player_persona = player_persona
        self.need_full_level = need_full_level

    def run(self):
        cur = self.config.START_NODE
        data = []
        self.director.update(None)
        cur = self._fit(cur, data, self.player_persona, self.playthroughs)

        return data
   