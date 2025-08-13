"""ReceivingMetrics class for representing nfl receivers (and other players who may have caught the ball).

Classes:
    ReceivingMetrics: A Pydantic data model representing weekly receiving metrics
"""
import re
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ReceivingMetrics(BaseModel):
    """A Pydantic model representing NFL receiving metrics at the week and player level.

    This model captures detailed receiving statistics for players, primarily wide receivers, but also others who may receive
    (e.g., RBs, TEs, QBs), as derived from seasonal or weekly NFL data. It is designed to validate and parse data from sources
    like the NGS receiving sample CSV, with fields aligned to the Player, PassingMetrics, and RushingMetrics models for integration.

    Attributes:
        gsis_id (str): The NFLverse GSIS player ID (e.g., '00-0034407').
        season (int): The NFL season year (e.g., 2024).
        season_type (str): The type of season (e.g., 'REG' for regular season, 'POST' for postseason).
        week (int): The week of the season (0 for season-level aggregation).
        position (str): The player's position (e.g., 'WR', 'RB', 'TE').
        team_abbr (str): The team abbreviation (e.g., 'ATL' for Atlanta Falcons).
        avg_cushion (float): Average cushion (distance from defender) at catch point (yards).
        avg_separation (float): Average separation from defender at catch point (yards).
        avg_intended_air_yards (float): Average air yards on targeted passes.
        percent_share_of_intended_air_yards (float): Percentage of team's intended air yards.
        receptions (int): Total receptions.
        targets (int): Total targets (pass attempts directed at the player).
        catch_percentage (float): Percentage of targets caught (receptions/targets * 100).
        yards (int): Total receiving yards.
        rec_touchdowns (int): Total receiving touchdowns.
        avg_yac (float): Average yards after catch per reception.
        avg_expected_yac (float): Average expected yards after catch per reception.
        avg_yac_above_expectation (float): Average yards after catch above expected per reception.
    """
    gsis_id: str = Field(min_length=10, max_length=10, frozen=True)
    season: int = Field(ge=1999, le=2025, frozen=False)
    season_type: str = Field(min_length=3, max_length=4, frozen=False)
    week: int = Field(ge=0, le=18, frozen=False)
    position: str = Field(min_length=1, max_length=3, frozen=False)
    team_abbr: str = Field(min_length=2, max_length=3, frozen=False)
    avg_cushion: float = Field(ge=0, frozen=False)
    avg_separation: float = Field(ge=0, frozen=False)
    avg_intended_air_yards: float = Field(frozen=False)
    percent_share_of_intended_air_yards: float = Field(ge=0, le=100, frozen=False)
    receptions: int = Field(ge=0, frozen=False)
    targets: int = Field(ge=0, frozen=False)
    catch_percentage: float = Field(ge=0, le=100, frozen=False)
    yards: int = Field(frozen=False)
    rec_touchdowns: int = Field(ge=0, frozen=False)
    avg_yac: float = Field(frozen=False)
    avg_expected_yac: float = Field(frozen=False)
    avg_yac_above_expectation: float = Field(frozen=False)

    @field_validator('gsis_id')
    def validate_gsis_id(
        cls,
        v: str
    ) -> str:
        """Validate that gsis_id matches the format ##-####### (e.g., '00-0034407')."""
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
        'receptions',
        'targets',
        'rec_touchdowns',
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

    @field_validator(
        'catch_percentage',
        mode='before'
    )
    def validate_catch_percentage(
        cls,
        v: float,
        values: dict
    ) -> float:
        """Validate that catch_percentage matches receptions/targets * 100 within a small margin."""
        if 'receptions' in values and 'targets' in values:
            receptions = values['receptions']
            targets = values['targets']
            if targets > 0:
                expected_catch_pct = (receptions / targets) * 100
                if abs(v - expected_catch_pct) > 0.01:  # Allow small floating-point errors
                    raise ValueError(
                        f"catch_percentage {v} does not match receptions {receptions} / targets {targets} * 100"
                    )
        return v

