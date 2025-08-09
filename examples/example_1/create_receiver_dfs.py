from src.fantasy_football.generate_data_frames import (
    create_receiver_dfs,
    create_all_dfs
)

all_data_frames = create_all_dfs()

qb_data_frames = create_receiver_dfs(all_data_frames)

x = 1