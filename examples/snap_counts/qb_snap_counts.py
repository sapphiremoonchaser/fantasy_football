"""QB Snap count analysis
"""
import pandas as pd

from fantasy_football.generate_data_frames import (
    create_passer_dfs,
    create_all_dfs
)

# Create quarterback snap count dataframe
all_data_frames = create_all_dfs()
qb_data_frames = create_passer_dfs(all_data_frames)
snap_count_df = qb_data_frames.snap_count_df

# Sum snap counts by season
snap_count_df = snap_count_df.groupby(['name', 'season'])['offense_snaps'].sum().reset_index()

# Pivot so that snap counts by  year are columns
snap_count_df_pivot = snap_count_df.pivot(
    index='name',
    columns='season',
    values='offense_snaps'
).reset_index()

# Rename columns to include _snaps
snap_count_df_pivot.columns = ['name'] + [f"{year}_snaps" for year in snap_count_df_pivot.columns[1:]]

# Sort columns
snap_count_df_pivot = snap_count_df_pivot[
    [
        'name',
        '2020_snaps',
        '2021_snaps',
        '2022_snaps',
        '2023_snaps',
        '2024_snaps'
    ]
]

x = 1