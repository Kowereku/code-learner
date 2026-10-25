from datetime import datetime

from pydantic import BaseModel


class BadgeRead(BaseModel):
    """A badge with the user's progress; awarded_at is null until it is earned."""

    code: str
    family: str
    goal: int
    progress: int
    awarded_at: datetime | None = None
