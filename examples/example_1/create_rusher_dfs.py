from src.fantasy_football.generate_data_frames import (
    create_rusher_dfs,
    create_all_dfs
)

all_data_frames = create_all_dfs()

rb_data_frames = create_rusher_dfs(all_data_frames)

player_id_df = rb_data_frames.player_id_df

weekly_roster_df = rb_data_frames.weekly_roster_df

weekly_stats_df = rb_data_frames.weekly_stats_df

snap_count_df = rb_data_frames.snap_count_df

ngs_rushing_df = rb_data_frames.ngs_rushing_df

x = 1