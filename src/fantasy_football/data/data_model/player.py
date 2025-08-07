"""Player class for representing nfl players.

Classes:
    Player: A Pydantic model representing an nfl player with field constraints for age, weight, height,
            a validator to calculate age, and properties to track if the player is currently active
            and first string.
"""
from pydantic import (
    BaseModel,
    Field,
    field_validator
)
import re
import nfl_data_py as nfl


class Player(BaseModel):
    """A model representing an nfl player.

    Args:
        player_id (str): the nflverse player id
        espn_id (int): espn identifier
        pfr_id (str): pfr id (for snap counts)
        status (str): whether or not the player is active
        team_abbr (str): the team the player currently plays for
        position (str): one of ('QB', 'RB', 'WR', 'TE', 'DEF')
        height (float): player's height (inches)
        weight (int): player's weight (pounds)
        college (str): college the player was drafted from
        years_exp (int): years played in the nfl
        age (float): age of the player
        offense_snaps (int): number of offense snaps (snap_counts)
        offense_pct (float): number of offense points per week (snap_counts)
        fantasy_points (float): number of fantasy points per week (weekly)
        fantasy_points_ppr (float): number of fantasy_points per week (weekly)

    """
    player_id: str = Field(min_length=10, max_length=10, frozen=True)
    espn_id: int = Field(frozen=True)
    pfr_id: str = Field(min_length=1, frozen=True)
    player_name: str = Field(min_length=1, frozen=True)
    status: str = Field(min_length=2, max_length=3, frozen=False)
    team_abbr: str = Field(min_length=2, max_length=3, frozen=False)
    position: str = Field(min_length=1, max_length=3, frozen=False)
    height: float = Field(gt=60, lt=90, frozen=False)
    weight: float = Field(gt=150, lt=450, frozen=False)
    college: str = Field(min_length=1, frozen=True)
    years_exp: int = Field(frozen=False)
    age: float = Field(ge=18, frozen=False)
    offense_snaps: int = Field(ge=0, frozen=False)
    offense_pct: float = Field(gt=0, frozen=False)
    fantasy_points: float = Field(frozen=False)
    fantasy_points_ppr: float = Field(frozen=False)

# Property for is active
@property
def is_active(self) -> bool:
    """Whether or not the player is currently active."""
    if self.status == 'ACT':
        return True
    else:
        return False

# Property for 1st string
@property
def is_first_string(self) -> bool:
    """Check if the player is the first-string player (pos_rank = 1) for their position and team.

    Returns:
        bool: True if the player's depth_team rank is 1, False otherwise or if data is unavailable.
    """
    try:
        # Import depth charts for the current season (2025)
        depth_charts = nfl.import_depth_charts([2025])

        # Filter for the player's team, position, and player_id
        player_depth = depth_charts[
            (depth_charts['espn_id'] == self.espn_id) &
            (depth_charts['team'] == self.team) &
            (depth_charts['position'] == self.position)
        ]

        # Check if depth_pos == 1 (first-string)
        if not player_depth.empty and player_depth['depth_pos'].iloc[0] == 1:
            return True

        return False

    except Exception as e:
        print(f"Error fetching depth chart for player {self.player_id}: {e}")
        return False

# validator for player id format ##_#######
@field_validator('player_id')
def validate_player_id(
        cls,
        v: str
) -> str:
    """Validate that player_id matches the format ##_####### (two digits, underscore, seven digits)."""
    pattern = r'^\d{2}-\d{7}$'

    if not re.match(pattern, v):
        raise ValueError(f"Player ID {v} does not match format ##_#######.")

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
    'offense_snaps',
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
