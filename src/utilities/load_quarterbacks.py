"""Load dataframe with quarterback and related data.

"""
import nfl_data_py as nfl

from typing import List

def load_weekly_qb_data(
        years: List[int],
):
    columns =[
        'player_id',
        'position',
        'fantasy_points',
        'fantasy_points_ppr',
        'season_type',

    ]

    df = nfl.import_weekly_data(
        years=years,
        columns
    )