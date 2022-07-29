from typing import Tuple, List

from dataclasses import dataclass
from GDM.Graph import Node

@dataclass
class NGramNode(Node):
    designer_reward: int
    player_reward: int
    visited_count: int
    slices: Tuple[str]
    behavioral_characteristics: Tuple[float, float]
    prior: List[str]
    percent_completable: float = 0