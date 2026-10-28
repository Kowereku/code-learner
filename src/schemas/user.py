from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, computed_field

from src.core.levels import level_for_xp, xp_for_level
from src.model.track import Track


class UserBase(BaseModel):
    """Base user schema containing public attributes."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username",
        examples=["john_doe"],
    )
    email: EmailStr = Field(
        ..., description="Unique email address", examples=["john@example.com"]
    )


class UserCreate(UserBase):
    """Payload for registering a new user."""

    password: str = Field(
        ...,
        min_length=6,
        max_length=32,
        description="User password",
        examples=["strongpassword123"],
    )


class UserRead(UserBase):
    """Public user profile response representation."""

    id: int
    total_xp: int
    streak_days: int
    best_streak: int = 0
    track: Track | None = None
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def level(self) -> int:
        """Level reached with the total XP; computed, never stored."""
        return level_for_xp(self.total_xp)

    @computed_field
    @property
    def level_xp(self) -> int:
        """XP threshold of the current level."""
        return xp_for_level(self.level)

    @computed_field
    @property
    def next_level_xp(self) -> int:
        """XP threshold of the next level."""
        return xp_for_level(self.level + 1)


class UserTrackUpdate(BaseModel):
    """Payload for saving the learning area chosen on the Choice page."""

    track: Track
