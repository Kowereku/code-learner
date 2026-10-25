from datetime import datetime, timedelta, timezone

from src.crud.user import refresh_streak


def test_refresh_streak_resets_a_broken_streak(db, make_user):
    today = datetime.now(timezone.utc).date()
    user = make_user(streak_days=4, last_activity_date=today - timedelta(days=3))
    assert refresh_streak(db, user).streak_days == 0
