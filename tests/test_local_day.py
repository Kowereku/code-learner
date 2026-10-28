from datetime import date, datetime, timezone

from src.core.streak import local_today

# 23:30 UTC on 25 Oct is already 26 Oct in Warsaw (UTC+1 in winter).
LATE_EVENING_UTC = datetime(2026, 10, 25, 23, 30, tzinfo=timezone.utc)


def test_local_today_uses_the_users_time_zone():
    assert local_today("Europe/Warsaw", LATE_EVENING_UTC) == date(2026, 10, 26)


def test_local_today_falls_back_to_utc_without_a_time_zone():
    assert local_today(None, LATE_EVENING_UTC) == date(2026, 10, 25)


def test_local_today_falls_back_to_utc_for_an_unknown_time_zone():
    assert local_today("Mars/Olympus_Mons", LATE_EVENING_UTC) == date(2026, 10, 25)
