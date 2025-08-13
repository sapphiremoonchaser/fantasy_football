"""PassingMetrics class for representing nfl quarterbacks (and other players who may have passed the ball).

Classes:
    PassingMetrics: A Pydantic data model representing weekly passing metrics
"""
import re

from pydantic import (
    BaseModel,
    Field,
    field_validator
)

class PassingMetrics(BaseModel):
    """A Pydantic model representing NFL quarterback passing metrics at the week and player level.

    This model captures detailed passing statistics for quarterbacks, including metrics like average time to throw,
    air yards, completion percentages, and more, as derived from seasonal or weekly NFL data. It is designed to
    validate and parse data from sources like the provided NGS passing sample CSV.

    Attributes:
        gsis_id (str): the nflverse player id (player_gsis_id in next-gen-stats)
        season (int): The NFL season year (e.g., 2024).
        season_type (str): The type of season (e.g., 'REG' for regular season).
        week (int): The week of the season (0 for season-level aggregation).
        avg_time_to_throw (float): Average time (in seconds) taken to throw the ball. (ngs)
        avg_completed_air_yards (float): Average air yards on completed passes. (ngs)
        avg_intended_air_yards (float): Average intended air yards on all pass attempts. (ngs)
        avg_air_yards_differential (float): Difference between intended and completed air yards. (ngs)
        aggressiveness (float): Measure of aggressive passing tendencies (percentage). (ngs)
        max_completed_air_distance (float): Maximum air distance of a completed pass. (ngs)
        avg_air_yards_to_sticks (float): Average air yards relative to the first-down marker. (ngs)
        attempts (int): Total pass attempts. (ngs)
        pass_yards (float): Total passing yards. (ngs)
        pass_touchdowns (int): Total passing touchdowns. (ngs)
        interceptions (int): Total interceptions thrown. (ngs)
        passer_rating (float): Quarterback passer rating. (ngs)
        completions (int): Total completed passes. (ngs)
        completion_percentage (float): Percentage of passes completed. (ngs)
        expected_completion_percentage (float): Expected completion percentage based on play context. (ngs)
        completion_percentage_above_expectation (float): Difference between actual and expected completion percentage. (ngs)
        avg_air_distance (float): Average air distance of passes. (ngs)
        max_air_distance (float): Maximum air distance of any pass attempt. (ngs)
        sacks (int): Total number of sacks. (weekly)
        sack_yards (float): Total number of sack yards. (weekly)
        sack_fumbles (int): Total number of sack fumbles. (weekly)
        sack_fumbles_lost (int): Total number of sack fumbles lost. (weekly)
    """
    gsis_id: str = Field(min_length=10, max_length=10, frozen=True)
    season: int = Field(ge=1999, le=2025, frozen=False)
    season_type: str = Field(min_length=3, max_length=4, frozen=False)
    week: int = Field(ge=0, frozen=False)
    avg_time_to_throw: float = Field(ge=0, frozen=False)
    avg_completed_air_yards: float = Field(ge=0, frozen=False)
    avg_intended_air_yards: float = Field(ge=0, frozen=False)
    avg_air_yards_differential: float = Field(frozen=False)
    aggressiveness: float = Field(ge=0, frozen=False)
    max_completed_air_distance: float = Field(frozen=False)
    avg_air_yards_to_sticks: float = Field(frozen=False)
    attempts: int = Field(ge=0, frozen=False)
    pass_yards: float = Field(frozen=False)
    pass_touchdowns: int = Field(ge=0, frozen=False)
    interceptions: int = Field(ge=0, frozen=False)
    passer_rating: float = Field(frozen=False)
    completions: int = Field(ge=0, frozen=False)
    completion_percentage: float = Field(ge=0, frozen=False)
    expected_completion_percentage: float = Field(ge=0, frozen=False)
    completion_percentage_above_expectation: float = Field(frozen=False)
    avg_air_distance: float = Field(frozen=False)
    max_air_distance: float = Field(frozen=False)
    sacks: int = Field(ge=0, frozen=False)
    sack_yards: float = Field(ge=0, frozen=False)
    sack_fumbles: int = Field(ge=0, frozen=False)
    sack_fumbles_lost: int = Field(ge=0, frozen=False)

# validator for player id format ##_#######
@field_validator('gsis_id')
def validate_player_id(
        cls,
        v: str
) -> str:
    """Validate that player_id matches the format ##_####### (two digits, underscore, seven digits)."""
    pattern = r'^\d{2}-\d{7}$'

    if not re.match(pattern, v):
        raise ValueError(f"GSIS ID {v} does not match format ##_#######.")

    return v

# validate season type in ['REG', 'POST']
@field_validator('season_type')
def validate_season_type(
         cls,
         v: str
 ) -> str:
    """Validate that season_type is one of ['REG', 'POST']."""
    valid_types = ['REG', 'POST']
    if v not in valid_types:
        raise ValueError(f"Season type {v} is not in {valid_types}.")
    return v

 # Validate team abbreviation
@field_validator('team_abbr')
def validate_team_abbr(
        cls,
        v: str
) -> str:
    """Validate that team_abbr is a valid NFL team abbreviation."""
    valid_teams = [
        'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN',
        'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC', 'LA', 'LAC', 'LV', 'MIA',
        'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'PHI', 'PIT', 'SF', 'SEA', 'TB',
        'TEN', 'WAS'
    ]
    if v not in valid_teams:
        raise ValueError(f"Team abbreviation {v} is not a valid NFL team.")
    return v

# position in ['QB', 'RB', 'WR', 'TE']
@field_validator('position')
def validate_position(
        cls,
        v: str
) -> str:
    """Validate that position is one of ['QB', 'RB', 'WR', 'TE']."""
    valid_positions = ['QB', 'RB', 'WR', 'TE']

    if v not in valid_positions:
        raise ValueError(f"Your position {v} is not in ['QB', 'RB', 'WR', 'TE'].")

    return v

# Convert int fields to int
@field_validator(
    'attempts',
    'pass_touchdowns',
    'interceptions',
    'completions',
    'sacks',
    'sack_fumbles',
    'sack_fumbles_lost',
    mode='before'
)
def to_int(
        cls,
        v: any,
        field: str
) -> int:
    """Convert numeric fields to integers, handling float or string inputs."""
    if isinstance(v, int):
        return v
    try:
        return int(float(v))
    except (ValueError, TypeError):
        raise ValueError(
            f"{field} must be convertible to an integer, got {v}")

