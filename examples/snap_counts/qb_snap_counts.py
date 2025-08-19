"""QB Snap count analysis
"""
from fantasy_football.generate_data_frames import (
    create_passer_dfs,
    create_all_dfs
)

from snap_count_functions import (
    create_snap_counts_by_year_df,
    plot_snap_counts
)

# Create quarterback snap count dataframe
all_data_frames = create_all_dfs()
qb_data_frames = create_passer_dfs(all_data_frames)
snap_count_df = qb_data_frames.snap_count_df

# Get snap counts by year filtered to qualifying players
# non-rookie, at least 1 year with snap counts over 66th percentile
qb_snap_counts_by_year = create_snap_counts_by_year_df(snap_count_df)

plot_snap_counts(qb_snap_counts_by_year)

x = 1