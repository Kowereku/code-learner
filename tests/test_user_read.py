from datetime import date, datetime, timedelta, timezone

from src.crud.user import user_read
from src.model.user import User

TODAY = date(2026, 10, 25)


def user(**fields) -> User:
    """A user that is never saved: reading it must not need the database."""
    defaults = dict(
        id=1,
        username="probe",
        email="probe@example.com",
        password="x",
        total_xp=0,
        best_streak=4,
        is_admin=False,
        created_at=datetime(2026, 10, 1, tzinfo=timezone.utc),
    )
    return User(**(defaults | fields))


def test_user_read_shows_a_broken_streak_as_zero():
    probe = user(streak_days=4, last_activity_date=TODAY - timedelta(days=3))
    assert user_read(probe, TODAY).streak_days == 0


def test_user_read_keeps_a_streak_active_yesterday():
    probe = user(streak_days=4, last_activity_date=TODAY - timedelta(days=1))
    assert user_read(probe, TODAY).streak_days == 4


def test_user_read_does_not_change_the_stored_streak():
    probe = user(streak_days=4, last_activity_date=TODAY - timedelta(days=3))
    user_read(probe, TODAY)
    assert probe.streak_days == 4


def test_user_read_includes_the_level():
    read = user_read(user(total_xp=340, streak_days=0, last_activity_date=None), TODAY)
    assert (read.level, read.level_xp, read.next_level_xp) == (3, 300, 600)
