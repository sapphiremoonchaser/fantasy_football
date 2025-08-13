from typing import NamedTuple

from pandas import DataFrame


class PasserDataFrames(NamedTuple):
    """This is a named tuple class that
       stores all the data frames from all
       sources. HOWEVER, the data frames
       have been filtered down to just
       QBs.

       Note: This is used as a return type for
             some functions.

       Note: This is the same as the AllDataFrames
             class, but just here to have a different
             name for the class.
    """
    player_id_df: DataFrame
    weekly_roster_df: DataFrame
    weekly_stats_df: DataFrame
    snap_count_df: DataFrame
    sacks_df: DataFrame
    ngs_passing_df: DataFrame