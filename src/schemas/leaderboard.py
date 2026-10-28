from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    """One ranked user: only what the ranking shows, nothing private."""

    position: int
    username: str
    level: int
    total_xp: int
    is_me: bool


class LeaderboardRead(BaseModel):
    """The top ranks plus the current user's own row (null while they have no XP)."""

    top: list[LeaderboardEntry] = []
    me: LeaderboardEntry | None = None
