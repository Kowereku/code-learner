from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.core.levels import level_for_xp
from src.model.user import User
from src.schemas.leaderboard import LeaderboardEntry, LeaderboardRead

TOP_POSITIONS = 10


def rank_of(db: Session, total_xp: int) -> int | None:
    """Position for this much XP: 1 + users with strictly more XP. Users without XP are unranked."""
    if total_xp <= 0:
        return None
    ahead = db.scalar(select(func.count()).select_from(User).where(User.total_xp > total_xp))
    return ahead + 1


def _entry(position: int, username: str, total_xp: int, is_me: bool) -> LeaderboardEntry:
    return LeaderboardEntry(
        position=position,
        username=username,
        level=level_for_xp(total_xp),
        total_xp=total_xp,
        is_me=is_me,
    )


def get_leaderboard(db: Session, user: User) -> LeaderboardRead:
    """Return the first ten ranked users (ties share a position) and the user's own row.

    The list is capped at ten rows even when many users tie; the frontend pins the
    user's own row below it whenever they aren't among those rows. Both come from one
    query, so the list and the user's own row always agree.
    """
    ranked = (
        select(
            User.id,
            User.username,
            User.total_xp,
            func.rank().over(order_by=User.total_xp.desc()).label("position"),
            func.row_number().over(order_by=(User.total_xp.desc(), User.id)).label("row"),
        )
        .where(User.total_xp > 0)
        .subquery()
    )
    rows = db.execute(
        select(ranked)
        .where((ranked.c.row <= TOP_POSITIONS) | (ranked.c.id == user.id))
        .order_by(ranked.c.row)
    ).all()
    mine = next((row for row in rows if row.id == user.id), None)
    return LeaderboardRead(
        top=[
            _entry(row.position, row.username, row.total_xp, row.id == user.id)
            for row in rows
            if row.row <= TOP_POSITIONS
        ],
        me=_entry(mine.position, mine.username, mine.total_xp, True) if mine else None,
    )
