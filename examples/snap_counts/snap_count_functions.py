"""Functions for snap_count analysis
"""
import matplotlib.pyplot as plt

import pandas as pd

from typing import List

from pandas.io.sas.sas_constants import text_block_size_length


def _has_qualifying_year(
        row: pd.Series,
        percentile_threshold: float,
        snap_cols: List[str]
) -> bool:
    """Helper function to count years above percentile threshold.

    :param row: a row from the DataFrame containing snap counts
    :param percentile_threshold: minimum value to include
    ":param snap_cols: List of column names to include
    :return int: number of years above percentile
    """
    return any(row[col] > percentile_threshold for col in snap_cols)

def create_snap_counts_by_year_df(
        df: pd.DataFrame,
) -> pd.DataFrame:
    """Create dataframe where years are columns and values are snap counts.
        The returned dataframe only includes current players (players who
        started last season). We'll also use a helper function to remove
        any players whose number of snap count have not been above the top
        66th percentile in any of the last 5 years.

    :param df: Dataframe containing name, season, and snap_count
    :return: Dataframe with snap counts by year for current players
    """
    # sum offensive snaps by season and reset index
    df = df.groupby(
        [
            'name',
            'season',
        ]
    )[
        'offense_snaps'
    ].sum().reset_index()

    # Pivot so that snap counts by year are columns
    df = df.pivot(
        index='name',
        columns='season',
        values='offense_snaps',
    ).reset_index()

    # Rename columns to include _snaps
    df.columns = ['name'] + [f"{int(year)}_snaps" for year in df.columns[1:]]

    # Remove QB's with no snaps in 2024
    df = df.dropna(subset=['2024_snaps'])

    # Fill the rest of the NaN values with 0
    df = df.fillna(0)

    # Identify snap count columns (YYYY_snaps)
    snap_cols: List[str] = [col for col in df.columns if col.endswith('_snaps')]

    # Raise ValueError if no yearly columns found
    if not snap_cols:
        raise ValueError("No snap count columns found. Columns should follow 'YYYY_snaps'")

    # Sort yearly columns t omake sure most recent is last
    snap_cols.sort(
        key=lambda x: int(x.split('_')[0])
    )

    # Calculate the 66th percentile of the most recent year's snaps across all players
    most_recent_year_col: str = snap_cols[-1]

    percentile_66: float = df[
        most_recent_year_col
    ].quantile(0.66)

    # Filter players with at least 1 qualifying year
    qualifying_players: pd.DataFrame
    qualifying_players = df[
        df.apply(
            _has_qualifying_year,
            axis=1,
            percentile_threshold=percentile_66,
            snap_cols=snap_cols,
        )
    ]

    return qualifying_players


def plot_snap_counts(
        df: pd.DataFrame
) -> None:
    """Generate a line graph of snap counts by year for current players.

    :param df: Dataframe with name and yearly snap count columns
    :return:
    """
    # Dynamically identify snap count column
    snap_cols: List[str] = [col for col in df.columns if col.endswith('_snaps')]
    years: List[int] = [int(col.split('_')[0]) for col in snap_cols]

    # Melt the dataframe to long format for plotting
    melted_df: pd.DataFrame = pd.melt(
        df,
        id_vars=['name'],
        value_vars=snap_cols,
        var_name='year',
        value_name='snaps'
    )

    melted_df['year'] = melted_df['year'].apply(lambda x: int(x.split('_')[0]))

    # Create the plot
    plt.figure(figsize=[12, 6])
    texts: List[plt.Text] = []
    for name in melted_df['name'].unique():
        player_data = melted_df[melted_df['name'] == name]
        line, = plt.plot(
            player_data['year'],
            player_data['snaps'],
            marker='o'
        )

        # Label last point with player name
        last_point = player_data.iloc[-1]
        text = plt.annotate(
            name,
            (
                last_point['year'],
                last_point['snaps']
            ),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=8,
            color=line.get_color()
        )
        texts.append(text)

    plt.xlabel('Year')
    plt.ylabel('Snaps')
    plt.title('Snap counts by year')
    plt.grid(True)
    plt.xticks(years)
    plt.tight_layout()

    # Display the plot
    plt.show()