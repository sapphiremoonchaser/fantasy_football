import nfl_data_py as nfl
from fantasy_football.data.named_tuple.all_data_frames import AllDataFrames
from fantasy_football.data.named_tuple.qb_data_frames import QbDataFrames


def create_all_dfs() -> AllDataFrames:
    """This function creates an instance of the
       AllDataFrames class, which stores all the
       data frames from all the sources.
    :return: AllDataFrames
    """

    # player_id data
    player_id_df = nfl.import_ids(
        columns=[
            'gsis_id',
            'espn_id',
            'pfr_id',
            'name',
            'team',
            'position',
            'height',
            'weight',
            'college',
            'age',
            'draft_year'
        ]
    )

    # Filter player_id_df to positions ['QB', 'RB', 'WR', 'TE']
    player_id_df = player_id_df[player_id_df['position'].isin(['QB', 'RB', 'WR', 'TE'])]

    # Data from the weekly roster
    weekly_roster_df = nfl.import_weekly_rosters(
        years=[2020, 2021, 2022, 2023, 2024]
    )

    # Filter to active only and positions ['QB', 'RB', 'WR', 'TE']
    weekly_roster_df = weekly_roster_df[weekly_roster_df['status'] == 'ACT']
    weekly_roster_df = weekly_roster_df[weekly_roster_df['position'].isin(['QB', 'RB', 'WR', 'TE'])]

    # Keep only desired columns
    weekly_roster_df = weekly_roster_df[
        [
            'player_id', # Same as gsis_id
            'season',
            'week',
            'status',
            'years_exp'
        ]
    ]

    # Snap Count data
    snap_count_df = nfl.import_snap_counts(
        years=[2020, 2021, 2022, 2023, 2024],
    )

    # Filter by position
    snap_count_df = snap_count_df[snap_count_df['position'].isin(['QB', 'RB', 'WR', 'TE'])]

    # drop un-used columns
    snap_count_df = snap_count_df.drop(
        columns=[
            'game_id',
            'pfr_game_id',
            'game_type',
            'player',
            'position',
            'team',
            'opponent',
            'defense_snaps',
            'defense_pct',
            'st_snaps',
            'st_pct'
        ]
    )


    # Weekly stats df
    weekly_stats_df = nfl.import_weekly_data(
        years=[2020, 2021, 2022, 2023, 2024],
        downcast=True
    )

    # Filter to desired positions
    weekly_stats_df = weekly_stats_df[weekly_stats_df['position'].isin(['QB', 'RB', 'WR', 'TE'])]

    # Keep only desired columns
    weekly_stats_df = weekly_stats_df[
        [
            'player_id',
            'season',
            'week',
            'fantasy_points',
            'fantasy_points_ppr'
        ]
    ]

    return AllDataFrames(
        player_id_df=player_id_df,
        weekly_roster_df=weekly_roster_df,
        snap_count_df=snap_count_df,
        weekly_stats_df=weekly_stats_df,
    )


def create_qb_dfs(
    all_data_frames: AllDataFrames,
) -> QbDataFrames:
    """This function filters down all the data in all
       the data frames to just be data about Qbs.

    :param all_data_frames: AllDataFrames
    :return: QbDataFrames
    """

    # ToDo: Filter player_id


    # ToDo: filter weekly roster


    # ToDo: filter snap count


    # ToDo: filter weekly stats



    # ToDo: ngs

    # Sacks data
    sacks_df = nfl.import_weekly_data(
        years=[2020, 2021, 2022, 2023, 2024],
        downcast=True
    )

    # QB only
    sacks_df = sacks_df[sacks_df['position'] == 'QB']

    # Keep only desired columns
    sack_df = sacks_df[
        [
            'player_id',
            'season',
            'week',
            'sacks',
            'sack_yards',
            'sack_fumbles',
            'sack_fumbles_lost'
        ]
    ]

    return QbDataFrames(
        sacks_df,
    )