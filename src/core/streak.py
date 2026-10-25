"""Daily streak rules. A day counts when the user completes any lesson; days are UTC dates."""

from datetime import date, timedelta


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
