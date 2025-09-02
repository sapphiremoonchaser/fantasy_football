import nfl_data_py as nfl
import pandas as pd
from typing import List

def fetch_schedule(
        seasons: List[int]
) -> pd.DataFrame:
    # Fetch the nfl schedule for the given years
    schedule = nfl.import_schedules(seasons)

    # Filter for regular season games
    schedule = schedule[
        schedule['game_type'] == 'REG'
    ]

    # Select and rename relevant columns
    df = schedule[[
        'game_id',
        'week',
        'gameday',
        'home_team',
        'away_team',
        'gametime'
    ]].copy()

    df = df.rename(columns={
        'game_id': 'Game ID',
        'week': 'Week',
        'gameday': 'Date',
        'home_team': 'Home Team',
        'away_team': 'Away Team',
        'gametime': 'Time'
    })

    # Replace missing time with 'TBD'
    df['Time'] = df['Time'].fillna('TBD')

    # Covert data to YYYY-MM-DD format
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

    # Sort by week and game ID for clarity
    df = df.sort_values(['Week', 'Game ID'])

    return df