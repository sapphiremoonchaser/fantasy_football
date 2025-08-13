from typing import List

from pandas import Series

from fantasy_football.data.data_model.player import Player
from fantasy_football.data.named_tuple.all_data_frames import AllDataFrames
from fantasy_football.data.named_tuple.passing_data_frames import PasserDataFrames
from fantasy_football.generate_data_frames import (
    create_all_dfs,
    create_passer_dfs,
)


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
    qb_data_frames: PasserDataFrames = create_passer_dfs(
        all_data_frames=all_data_frames,
    )

    # Everything except snap_count uses gsis_id
    player_ids: List[str] = all_data_frames.player_id_df['gsis_id'].tolist()

    # Create a list to store the QB data models.
    qb_data_models: List[Player] = []

    # Loop over all the names.
    player_id: str
    for player_id in player_ids:
        # Player_id dataframe
        player_id_df: Series = qb_data_frames.player_id_df[
            qb_data_frames.player_id_df['gsis_id'] == player_id
        ]

        # Weekly Roster dataframe
        filter_qb_df_2: Series = filter_qb_df_2[
            filter_qb_df_2['player_id'] == player_id
        ]

        # Snap Counts dataframe
        filter_qb_df_3: Series = filter_qb_df_3[
            filter_qb_df_3['player_id'] == player_id
        ]

        # Weekly Stats Dataframe
        filter_qb_df_4: Series = filter_qb_df_4[
            filter_qb_df_4['player_id'] == player_id
        ]

        # Sacks df
        filter_qb_df_5: Series = filter_qb_df_5[
            filter_qb_df_5['player_id'] == player_id
        ]

        # Next-gen-stats dataframe
        filter_qb_df_6: Series = filter_qb_df_6[
            filter_qb_df_6['player_id'] == player_id
        ]



        # Call the class method here.
        qb_data_models.append(
            Player.create_from_qb_series(
                player_id_df=player_id_df,
                filter_qb_df_2=filter_qb_df_2,
                filter_qb_df_3=filter_qb_df_3,
                filter_qb_df_4=filter_qb_df_4,
                filter_qb_df_5=filter_qb_df_5,
                filter_qb_df_6=filter_qb_df_6
            ),
        )


    # Todo: Add Similar code for each position.
