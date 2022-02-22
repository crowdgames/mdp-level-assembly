from Utility import slices_to_rows, rows_to_slices
from dungeongrams.dungeongrams import percent_playable, FLAW_NO_FLAW
from os.path import join

WRAPS = False
TRANSPOSE = False
START_NODE = '0,0,0'
PADDING_SIZE = 2
NAME = 'DungeonGram'

BASE_DIR = join('.', 'GramElitesData', 'DungeonData', 'gram_elites')
S = '0_0_0'

def columns_into_rows(columns):
    column_length = len(columns[0])
    rows = ["" for _ in range(column_length)]

    for col in columns:
        i = column_length - 1
        j = 0

        while i >= 0:
            rows[j] = f'{rows[j]}{col[i]}'

            i -= 1
            j += 1

    return rows

def get_furthest_xy(lvl):
    return percent_playable(slices_to_rows(lvl, False), False, True, False, FLAW_NO_FLAW), 0
