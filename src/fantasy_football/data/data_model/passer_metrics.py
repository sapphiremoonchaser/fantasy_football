"""PasserMetrics class for representing nfl quarterbacks (and other players who may have passed the ball).

Classes:
    Player: A Pydantic model representing an nfl player with field constraints for age, weight, height,
            a validator to calculate age, and properties to track if the player is currently active
            and first string.
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
        player_id (str): the nflverse player id (player_gsis_id in next-gen-stats)
        season (int): The NFL season year (e.g., 2024).
        season_type (str): The type of season (e.g., 'REG' for regular season).
        week (int): The week of the season (0 for season-level aggregation).
        position (str): The player's position (e.g., 'QB').
        team (str): The team abbreviation (e.g., 'PHI' for Philadelphia Eagles).
        avg_time_to_throw (float): Average time (in seconds) taken to throw the ball.
        avg_completed_air_yards (float): Average air yards on completed passes.
        avg_intended_air_yards (float): Average intended air yards on all pass attempts.
        avg_air_yards_differential (float): Difference between intended and completed air yards.
        aggressiveness (float): Measure of aggressive passing tendencies (percentage).
        max_completed_air_distance (float): Maximum air distance of a completed pass.
        avg_air_yards_to_sticks (float): Average air yards relative to the first-down marker.
        attempts (int): Total pass attempts.
        pass_yards (float): Total passing yards.
        pass_touchdowns (int): Total passing touchdowns.
        interceptions (float): Total interceptions thrown.
        passer_rating (float): Quarterback passer rating.
        completions (int): Total completed passes.
        completion_percentage (float): Percentage of passes completed.
        expected_completion_percentage (float): Expected completion percentage based on play context.
        completion_percentage_above_expectation (float): Difference between actual and expected completion percentage.
        avg_air_distance (float): Average air distance of passes.
        max_air_distance (float): Maximum air distance of any pass attempt.
    """
    player_id: str = Field(min_length=10, max_length=10, frozen=True)
    season: int = Field(ge=1999, le=2025, frozen=True)
    season_type: str = Field(min_length=3, max_length=3, frozen=True)
    week: int = Field(gt=0, frozen=True)
    position: str = Field(frozen=True)
    team: str = Field(min_length=2, max_length=3, frozen=True)
    avg_time_to_throw: float = Field(ge=0, frozen=True)
    avg_completed_air_yards: float = Field(ge=0, frozen=True)
    avg_intended_air_yards: float = Field(ge=0, frozen=True)
    avg_air_yards_differential: float = Field(frozen=True)
    aggressiveness: float = Field(ge=0, frozen=True)
    max_completed_air_distance: float = Field(frozen=True)
    avg_air_yards_to_sticks: float = Field(frozen=True)
    attempts: int = Field(ge=0, frozen=True)
    pass_yards: float = Field(frozen=True)
    pass_touchdowns: int = Field(ge=0, frozen=True)
    interceptions: int = Field(ge=0, frozen=True)
    passer_rating: float = Field(frozen=True)
    completions: int = Field(ge=0, frozen=True)
    completion_percentage: float = Field(ge=0, frozen=True)
    expected_completion_percentage: float = Field(ge=0, frozen=True)
    completion_percentage_above_expectation: float = Field(frozen=True)
    avg_air_distance: float = Field(frozen=True)
    max_air_distance: float = Field(frozen=True)

# validator for player id format ##_#######
@field_validator('player_id', mode='before')
def validate_player_id(
        cls,
        v: str
) -> str:
    """Validate that player_id matches the format ##_####### (two digits, underscore, seven digits)."""
    pattern = r'^\d{2}_\d{7}$'

    if not re.match(pattern, v):
        raise ValueError(f"Player ID {v} does not match format ##_#######.")

    return v

# position = QB
@field_validator('position', mode='before')
def validate_position(
        cls,
        v: str
) -> str:
    """Validate that position 'QB'."""
    if v != 'QB':
        raise ValueError(f"Your position {v} is not 'QB'.")

    return v

# change attempts to int before processing in the data model
@field_validator('attempts', mode='before')
def attempts_to_int(
        cls,
        v: str
) -> int:
    """Change attempts to an integer in case in comes in as a float."""
    if isinstance(v, int):
        return v
    else:
        try:
            return int(v)
        except ValueError:
            raise ValueError(f"Attempts must be an integer. You entered: {v}")

# change pass_touchdowns to int before processing in the data model
@field_validator('pass_touchdowns', mode='before')
def pass_touchdowns_to_int(
        cls,
        v: str
) -> int:
    """Change pass_touchdowns to an integer in case in comes in as a float."""
    if isinstance(v, int):
        return v
    else:
        try:
            return int(v)
        except ValueError:
            raise ValueError(f"Pass Touchdowns must be an integer. You entered {v}")

# change interceptions to int before processing in the data model
@field_validator('interceptions', mode='before')
def interceptions_to_int(
        cls,
        v: str
) -> int:
    """Change interceptions to an integer in case in comes in as a float."""
    if isinstance(v, int):
        return v
    else:
        try:
            return int(v)
        except ValueError:
            raise ValueError(f"Interceptions must be an integer. You entered {v}")

# change completions to int before processing in the data model
@field_validator('completions', mode='before')
def completions_to_int(
        cls,
        v: str
) -> int:
    """Change completions to an integer in case in comes in as a float."""
    if isinstance(v, int):
        return v
    else:
        try:
            return int(v)
        except ValueError:
            raise ValueError(f"Completions must be an integer. You entered {v}")

