from typing import List

from pandas import Series

from fantasy_football.data.data_model.player import Player
from fantasy_football.data.named_tuple.all_data_frames import AllDataFrames
from fantasy_football.data.named_tuple.qb_data_frames import QbDataFrames
from fantasy_football.generate_data_frames import create_all_dfs, \
    filter_dfs_for_qbs


def create_data_models():
    """This function is kinda like your main
       function, at least for now. It calls
       everything to generate the data models.

       I left the return type as undefined due to this
       not sure where your going with it
    """

    # Create all the dataframes from all sources.
    all_data_frames: AllDataFrames = create_all_dfs()

    # Filter down the dataframes to just the QBs.
    qb_data_frames: QbDataFrames = filter_dfs_for_qbs(
        all_data_frames=all_data_frames,
    )

    # Todo: create a list of qb names to filter
    #       against, this needs to be the same
    #       in all dataframes.
    qb_names: List[str] = []

    # Create a list to store the QB data models.
    qb_data_models: List[Player] = []

    # Loop over all the names.
    qb_name: str
    for qb_name in qb_names:
        # Todo: You need to filter down the qb data frames to just
        #       the row in each qb df for that qb.
        filter_qf_df_1: Series = None # Fill in this syntax
        filter_qf_df_2: Series = None  # Fill in this syntax
        filter_qf_df_n: Series = None  # Fill in this syntax


        # Call the class method here.
        qb_data_models.append(
            Player.create_from_qb_series(
                filter_qf_df_1=filter_qf_df_1,
                filter_qf_df_2=filter_qf_df_2,
                filter_qf_df_n=filter_qf_df_n,
            ),
        )


    # Todo: Add Similar code for each position.
