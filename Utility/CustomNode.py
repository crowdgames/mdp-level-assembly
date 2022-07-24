from typing import Tuple

from dataclasses import dataclass
from GDM.Graph import Node

@dataclass
class CustomNode(Node):
    designer_reward: int
    player_reward: int
    visited_count: int
    slices: Tuple[str]
    behavioral_characteristics: Tuple[float, float]
    percent_completable: float = 0