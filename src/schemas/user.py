from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


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
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
