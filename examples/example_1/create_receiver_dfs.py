from src.fantasy_football.generate_data_frames import (
    create_rusher_dfs,
    create_all_dfs
)

all_data_frames = create_all_dfs()

rb_data_frames = create_rusher_dfs(all_data_frames)

x = 1