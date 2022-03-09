from Utility import slices_to_rows, rows_to_slices
from dungeongrams.dungeongrams import percent_playable, FLAW_NO_FLAW
from os.path import join

WRAPS = False
TRANSPOSE = False
START_NODE = '0,0,0'
PADDING_SIZE = 2
NAME = 'DungeonGram'
MAX_BC = None
NUM_BC = 2


BASE_DIR = join('.', 'GramElitesData', 'DungeonData', 'gram_elites')
S = '0_0_0'


def get_furthest_xy(lvl):
    return percent_playable(slices_to_rows(lvl, False), False, True, False, FLAW_NO_FLAW), 0
