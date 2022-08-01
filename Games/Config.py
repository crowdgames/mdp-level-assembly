from dataclasses import dataclass
from typing import Callable, Set, List, Tuple
from Utility import RewardType


@dataclass
class Config:
    WRAPS: bool
    TRANSPOSE: bool
    START_NODE: str
    PADDING_SIZE: int 
    NAME: str
    MAX_BC: int 
    NUM_BC: int
    REWARD_TYPE: RewardType
    ALLOW_EMPTY_LINK: bool
    GRAMMAR_SIZE: int
    TRAINING_LEVELS_DIR: str

    SOLIDS: Set[str]
    JUMPS: List[List[Tuple[int, int]]]

    BASE_DIR: str
    TRAINING_LEVELS_DIR: str

    # functions
    read_file: Callable[[str], List[str]]
    get_furthest_xy: Callable[[List[str]], Tuple[int, int]] # update
    player_reward: Callable[[List[str]], float]
    level_to_str: Callable[[List[str]], str]
    designer_reward: Callable[[List[str]], float]