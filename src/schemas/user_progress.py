from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class UserProgressUpdate(BaseModel):
    """Input payload for updating or initiating user progress in a lesson."""

    status: str | None = Field(
        default=None,
        description="Lesson status (e.g. 'in_progress', 'completed')",
        examples=["in_progress"],
    )
    last_position: Any | None = Field(
        default=None,
        description="Flexible position identifier (e.g. block ID, timestamp, exercise step, or custom JSON)",
        examples=["step_2"],
    )


class UserProgressRead(BaseModel):
    """Output schema representing the stored user progress for a lesson."""

    user_id: int
    lesson_id: int
    status: str
    last_position: Any | None = None
    completed_at: datetime | None = None
    mistakes_made: int = 0
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
