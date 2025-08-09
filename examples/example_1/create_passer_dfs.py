from src.fantasy_football.generate_data_frames import (
    create_passing_dfs,
    create_all_dfs
)

all_data_frames = create_all_dfs()

qb_data_frames = create_passing_dfs(all_data_frames)

x = 1