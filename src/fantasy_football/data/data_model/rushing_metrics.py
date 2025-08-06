"""RushingMetrics class for representing nfl running backs (and other players who may have ran the ball).

Classes:
    RushingMetrics: A Pydantic data model representing weekly rushing metrics
"""
import re
from pydantic import BaseModel, Field, field_validator

class RushingMetrics(BaseModel):
    """A Pydantic model representing NFL rushing metrics at the week and player level.

    This model captures detailed rushing statistics for players, primarily running backs, but also others who may rush
    (e.g., QBs, WRs in trick plays), as derived from seasonal or weekly NFL data. It is designed to validate and parse
    data from sources like the NGS rushing sample CSV, with fields aligned to the Player and PassingMetrics models for integration.

    Attributes:
        gsis_id (str): The NFLverse GSIS player ID (e.g., '00-0037263').
        season (int): The NFL season year (e.g., 2024).
        season_type (str): The type of season (e.g., 'REG' for regular season, 'POST' for postseason).
        week (int): The week of the season (0 for season-level aggregation).
        position (str): The player's position (e.g., 'RB', 'QB', 'WR').
        team_abbr (str): The team abbreviation (e.g., 'ATL' for Atlanta Falcons).
        efficiency (float): Measure of rushing efficiency.
        percent_attempts_gte_eight_defenders (float): Percentage of rush attempts against 8+ defenders.
        avg_time_to_los (float): Average time to the line of scrimmage (in seconds).
        rush_attempts (int): Total rush attempts.
        rush_yards (int): Total rushing yards.
        avg_rush_yards (float): Average yards per rush attempt.
        rush_touchdowns (int): Total rushing touchdowns.
        expected_rush_yards (float): Expected rushing yards based on play context.
        rush_yards_over_expected (float): Difference between actual and expected rushing yards.
        rush_yards_over_expected_per_att (float): Rushing yards over expected per attempt.
        rush_pct_over_expected (float): Percentage of rushes exceeding expected yards.
    """
    gsis_id: str = Field(min_length=10, max_length=10, frozen=True)
    season: int = Field(ge=1999, le=2025, frozen=False)
    season_type: str = Field(min_length=3, max_length=4, frozen=False)
    week: int = Field(ge=0, le=18, frozen=False)
    position: str = Field(min_length=1, max_length=3, frozen=False)
    team_abbr: str = Field(min_length=2, max_length=3, frozen=False)
    efficiency: float = Field(frozen=False)
    percent_attempts_gte_eight_defenders: float = Field(ge=0, le=100, frozen=False)
    avg_time_to_los: float = Field(ge=0, frozen=False)
    rush_attempts: int = Field(ge=0, frozen=False)
    rush_yards: int = Field(frozen=False)
    avg_rush_yards: float = Field(frozen=False)
    rush_touchdowns: int = Field(ge=0, frozen=False)
    expected_rush_yards: float = Field(frozen=False)
    rush_yards_over_expected: float = Field(frozen=False)
    rush_yards_over_expected_per_att: float = Field(frozen=False)
    rush_pct_over_expected: float = Field(ge=0, le=1, frozen=False)

    @field_validator('gsis_id')
    def validate_gsis_id(
        cls,
        v: str
    ) -> str:
        """Validate that gsis_id matches the format ##-####### (e.g., '00-0037263')."""
        pattern = r'^\d{2}-\d{7}$'
        if not re.match(pattern, v):
            raise ValueError(f"GSIS ID {v} does not match format ##-#######.")
        return v

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

    @field_validator('position')
    def validate_position(
        cls,
        v: str
    ) -> str:
        """Validate that position is one of ['QB', 'RB', 'WR', 'TE']."""
        valid_positions = ['QB', 'RB', 'WR', 'TE']
        if v not in valid_positions:
            raise ValueError(f"Position {v} is not in {valid_positions}.")
        return v

    @field_validator(
        'rush_attempts',
        'rush_yards',
        'rush_touchdowns',
        mode='before'
    )
    def to_int(
        cls,
        v: any,
        field: any
    ) -> int:
        """Convert numeric fields to integers, handling float or string inputs."""
        if isinstance(v, int):
            return v
        try:
            return int(float(v))
        except (ValueError, TypeError):
            raise ValueError(f"{field.name} must be convertible to an integer, got {v}")

    @field_validator('avg_rush_yards', mode='before')
    def validate_avg_rush_yards(
        cls,
        v: float,
        values: dict
    ) -> float:
        """Validate that avg_rush_yards matches rush_yards/rush_attempts within a small margin."""
        if 'rush_yards' in values and 'rush_attempts' in values:
            rush_yards = values['rush_yards']
            rush_attempts = values['rush_attempts']
            if rush_attempts > 0:
                expected_avg = rush_yards / rush_attempts
                if abs(v - expected_avg) > 0.01:  # Allow small floating-point errors
                    raise ValueError(
                        f"avg_rush_yards {v} does not match rush_yards {rush_yards} / rush_attempts {rush_attempts}"
                    )
        return v