from fantasy_football.generate_data_frames import (
    create_passer_dfs,
    create_all_dfs
)

all_data_frames = create_all_dfs()

qb_data_frames = create_passer_dfs(all_data_frames)

player_id_df = qb_data_frames.player_id_df

weekly_roster_df = qb_data_frames.weekly_roster_df

weekly_stats_df = qb_data_frames.weekly_stats_df

snap_count_df = qb_data_frames.snap_count_df

sack_df = qb_data_frames.sacks_df

ngs_passing_df = qb_data_frames.ngs_passing_df

x = 1
