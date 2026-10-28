"""Daily streak rules. A day counts when the user completes any lesson, in the user's own time zone."""

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def local_today(time_zone: str | None, now: datetime) -> date:
    """Return the user's calendar date for the UTC moment now; UTC when the zone is missing or unknown."""
    if time_zone:
        try:
            return now.astimezone(ZoneInfo(time_zone)).date()
        except (ZoneInfoNotFoundError, ValueError):
            pass
    return now.date()


def next_streak(last_activity: date | None, today: date, streak: int) -> int:
    """Return the streak after completing a lesson today."""
    if last_activity == today:
        return streak
    if last_activity == today - timedelta(days=1):
        return streak + 1
    return 1


def displayed_streak(last_activity: date | None, today: date, streak: int) -> int:
    """Return the streak to show: 0 once a whole day was skipped since the last activity."""
    if last_activity is None or last_activity < today - timedelta(days=1):
        return 0
    return streak
