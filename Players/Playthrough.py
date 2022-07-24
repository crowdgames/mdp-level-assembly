from typing import List, Dict
from .PlaythroughEntry import PlaythroughEntry

class Playthrough:
    def __init__(self):
        self.entries: List[PlaythroughEntry] = []

    def add(self, playthrough_entry: PlaythroughEntry):
        self.entries.append(playthrough_entry)

    def get_summary(self, nodes: List[str]) -> Dict:
        percent_complete = 0
        percent_player_reward = 0
        percent_design_reward = 0
        percent_total_reward = 0
        percent_reward = 0

        for entry in self.entries:
            percent_complete += entry.percent_completable
            percent_player_reward += entry.player_reward
            percent_design_reward += entry.designer_reward
            percent_total_reward += entry.total_reward
            percent_reward += entry.reward

        # percent_complete is based on how far the player should have been able to go.
        # The other two are based on what the player experienced.
        percent_complete /= len(nodes)
        percent_player_reward /= len(nodes)
        percent_design_reward /= len(nodes)
        percent_total_reward /= len(nodes)
        percent_reward /= len(nodes)

        return {
            'Playthrough': [e.to_dict() for e in self.entries],
            'percent_complete': percent_complete,
            'percent_player_reward': percent_player_reward,
            'percent_design_reward': percent_design_reward,
            'percent_total_reward': percent_total_reward,
            'percent_reward': percent_reward,
            'nodes_seen': len(self.entries),
            'nodes_available': len(nodes)
        }