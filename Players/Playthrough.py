class Playthrough:
    def __init__(self):
        self.entries = []

    def add(self, playthrough_entry):
        self.entries.append(playthrough_entry)

    def get_summary(self, nodes):
        percent_complete = 0
        percent_player_reward = 0
        percent_design_reward = 0
        percent_total_reward = 0

        for entry in self.entries:
            percent_complete += entry.percent_completable
            percent_player_reward += entry.player_reward
            percent_design_reward += entry.designer_reward
            percent_total_reward += entry.total_reward

        # percent_complete is based on how far the player should have been able to go.
        # The other two are based on what the player experienced.
        percent_complete /= len(nodes)
        percent_player_reward /= len(self.entries)
        percent_design_reward /= len(self.entries)
        percent_total_reward /= len(self.entries)

        return {
            'Playthrough': [e.to_dict() for e in self.entries],
            'percent_complete': percent_complete,
            'percent_player_reward': percent_player_reward,
            'percent_design_reward': percent_design_reward,
            'percent_total_reward': percent_total_reward,
        }