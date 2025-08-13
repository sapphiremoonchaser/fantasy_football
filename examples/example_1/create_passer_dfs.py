from fantasy_football.generate_data_frames import (
    create_passer_dfs,
    create_all_dfs
)

all_data_frames = create_all_dfs()

qb_data_frames = create_passer_dfs(all_data_frames)

x = 1
