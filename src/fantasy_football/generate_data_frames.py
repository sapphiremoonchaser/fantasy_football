import nfl_data_py as nfl
from fantasy_football.data.named_tuple.all_data_frames import AllDataFrames
from fantasy_football.data.named_tuple.passing_data_frames import QbDataFrames
from fantasy_football.data.named_tuple.rushing_data_frames import RbDataFrames
from fantasy_football.data.named_tuple.receiving_data_frames import WrDataFrames


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
            'position',
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
            'position',
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


def create_passing_dfs(
    all_data_frames: AllDataFrames,
) -> QbDataFrames:
    """This function filters down all the data in all
       the data frames to just be data about Qbs.

    :param all_data_frames: AllDataFrames
    :return: QbDataFrames
    """

    # Filter player_id
    player_id_df = all_data_frames.player_id_df
    player_id_df = player_id_df[player_id_df['position'] == 'QB']

    # Filter weekly roster
    weekly_roster_df = all_data_frames.weekly_roster_df
    weekly_roster_df = weekly_roster_df[weekly_roster_df['position'] == 'QB']

    # Filter snap count
    snap_count_df = all_data_frames.snap_count_df
    snap_count_df = snap_count_df[snap_count_df['position'] == 'QB']

    # Filter weekly stats
    weekly_stats_df = all_data_frames.weekly_stats_df
    weekly_stats_df = weekly_stats_df[weekly_stats_df['position'] == 'QB']

    # Sacks data
    sacks_df = nfl.import_weekly_data(
        years=[2020, 2021, 2022, 2023, 2024],
        downcast=True
    )

    # QB only
    sacks_df = sacks_df[sacks_df['position'] == 'QB']

    # Keep only desired columns
    sacks_df = sacks_df[
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

    # Next-Gen-Stats passing data
    ngs_passing_df = nfl.import_ngs_data(
        stat_type='passing',
        years=[2020, 2021, 2022, 2023, 2024],
    )

    # Keep only desired columns
    ngs_passing_df = ngs_passing_df[
        [
            'player_gsis_id',
            'season',
            'week',
            'avg_time_to_throw',
            'avg_completed_air_yards',
            'avg_intended_air_yards',
            'avg_air_yards_differential',
            'aggressiveness',
            'max_completed_air_distance',
            'avg_air_yards_to_sticks',
            'attempts',
            'pass_yards',
            'pass_touchdowns',
            'interceptions',
            'passer_rating',
            'completions',
            'completion_percentage',
            'expected_completion_percentage',
            'completion_percentage_above_expectation',
            'avg_air_distance',
            'max_air_distance'
        ]
    ]

    return QbDataFrames(
        player_id_df=player_id_df,
        weekly_roster_df=weekly_roster_df,
        weekly_stats_df=weekly_stats_df,
        snap_count_df=snap_count_df,
        sacks_df=sacks_df,
        ngs_passing_df=ngs_passing_df,
    )


def create_rushing_dfs(
    all_data_frames: AllDataFrames,
) -> RbDataFrames:
    """This function filters down all the data in all
       the data frames to just be data about rushers.

    :param all_data_frames: AllDataFrames
    :return: RbDataFrames
    """

    # Next-Gen-Stats rushing data
    ngs_rushing_df = nfl.import_ngs_data(
        stat_type='rushing',
        years=[2020, 2021, 2022, 2023, 2024],
    )

    # Keep only desired columns
    ngs_rushing_df = ngs_rushing_df[
        [
            'player_gsis_id',
            'season',
            'week',
            'efficiency',
            'percent_attempts_gte_eight_defenders',
            'avg_time_to_los',
            'rush_attempts',
            'rush_yards',
            'avg_rush_yards',
            'rush_touchdowns',
            'expected_rush_yards',
            'rush_yards_over_expected',
            'rush_yards_over_expected_per_att',
            'rush_pct_over_expected'
        ]
    ]

    return RbDataFrames(
        player_id_df=all_data_frames.player_id_df,
        weekly_roster_df=all_data_frames.weekly_roster_df,
        weekly_stats_df=all_data_frames.weekly_stats_df,
        snap_count_df=all_data_frames.snap_count_df,
        ngs_rushing_df=ngs_rushing_df
    )


def create_receiving_dfs(
    all_data_frames: AllDataFrames,
) -> WrDataFrames:
    """This function filters down all the data in all
       the data frames to just be data about receivers.

    :param all_data_frames: AllDataFrames
    :return: WrDataFrames
    """

    # Next-Gen-Stats rushing data
    ngs_rushing_df = nfl.import_ngs_data(
        stat_type='rushing',
        years=[2020, 2021, 2022, 2023, 2024],
    )

    # Keep only desired columns
    ngs_rushing_df = ngs_rushing_df[
        [
            'player_gsis_id',
            'season',
            'week',
            'avg_cushion',
            'avg_separation',
            'avg_intended_air_yards',
            'percent_share_of_intended_air_yards',
            'receptions',
            'targets',
            'catch_percentage',
            'yards',
            'rec_touchdowns',
            'avg_yac',
            'avg_expected_yac',
            'avg_yac_above_expectation'
        ]
    ]

    return WrDataFrames(
        player_id_df=all_data_frames.player_id_df,
        weekly_roster_df=all_data_frames.weekly_roster_df,
        weekly_stats_df=all_data_frames.weekly_stats_df,
        snap_count_df=all_data_frames.snap_count_df,
        ngs_rushing_df=ngs_rushing_df
    )