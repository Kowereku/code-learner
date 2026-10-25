from datetime import date

from src.core.streak import displayed_streak, next_streak

TODAY = date(2026, 10, 25)


def test_first_ever_activity_starts_at_one():
    assert next_streak(None, TODAY, 0) == 1


def test_same_day_keeps_streak():
    assert next_streak(TODAY, TODAY, 4) == 4


def test_next_day_extends_streak():
    assert next_streak(date(2026, 10, 24), TODAY, 4) == 5


def test_gap_resets_to_one():
    assert next_streak(date(2026, 10, 22), TODAY, 4) == 1


def test_displayed_streak_alive_yesterday():
    assert displayed_streak(date(2026, 10, 24), TODAY, 4) == 4


def test_displayed_streak_broken():
    assert displayed_streak(date(2026, 10, 23), TODAY, 4) == 0


def test_displayed_streak_never_active():
    assert displayed_streak(None, TODAY, 0) == 0
