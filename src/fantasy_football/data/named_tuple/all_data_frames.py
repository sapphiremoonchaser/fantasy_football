from typing import NamedTuple

from pandas import DataFrame


class AllDataFrames(NamedTuple):
    """This is a named tuple class that
       stores all the data frames from all
       sources.

       Note: This is used as a return type for
             some functions.
    """

    player_id_df: DataFrame
    snap_count_df: DataFrame
    weekly_roster_df: DataFrame
    weekly_stats_df: DataFrame