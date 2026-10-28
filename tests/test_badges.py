from src.core.badges import BADGES, Metrics, closest_next, earned_codes, progress

ZERO = Metrics(0, 0, 0, 0, 0)


def by_code(code):
    return next(b for b in BADGES if b.code == code)


def test_badges_in_order():
    assert [b.code for b in BADGES] == [
        "courses_1",
        "courses_5",
        "courses_10",
        "streak_3",
        "streak_5",
        "streak_10",
        "streak_30",
        "flawless_lesson",
        "perfect_quiz",
        "own_code_10",
        "own_code_50",
        "own_code_100",
        "level_3",
        "level_5",
        "level_10",
    ]


def test_level_badge_uses_level_metric():
    reached = earned_codes(Metrics(0, 0, 0, 0, 0, level=5))
    assert {"level_3", "level_5"} <= reached and "level_10" not in reached


def test_progress_is_capped_at_goal():
    assert progress(by_code("streak_3"), Metrics(0, 7, 0, 0, 0)) == 3


def test_earned_codes():
    assert earned_codes(Metrics(1, 4, 1, 0, 7)) == {"courses_1", "streak_3", "flawless_lesson"}


def test_closest_next_highest_share():
    m = Metrics(1, 4, 1, 0, 7, current_streak=4)
    assert closest_next(m, earned_codes(m)).code == "streak_5"


def test_unearned_streak_progress_follows_current_streak():
    # Best streak 2, then it broke; one day into the new streak the badge shows 1/3, not 2/3.
    assert progress(by_code("streak_3"), Metrics(0, 2, 0, 0, 0, current_streak=1)) == 1


def test_earned_streak_badge_shows_full_progress_after_break():
    assert progress(by_code("streak_3"), Metrics(0, 4, 0, 0, 0, current_streak=0)) == 3


def test_closest_next_ranks_streak_by_current_streak():
    # Best streak 4 but broken: own_code (7/10) is closer than streak_5 (0/5).
    m = Metrics(1, 4, 1, 0, 7, current_streak=0)
    assert closest_next(m, earned_codes(m)).code == "own_code_10"


def test_closest_next_tie_prefers_smaller_goal():
    assert closest_next(ZERO, set()).code == "courses_1"


def test_closest_next_none_when_all_earned():
    m = Metrics(10, 30, 1, 1, 100, level=10)
    assert closest_next(m, earned_codes(m)) is None


def test_fresh_user_has_no_level_badge_progress():
    # Level 1 is where everyone starts, so it doesn't count towards "Level 3".
    fresh = Metrics(0, 0, 0, 0, 0, level=1)
    assert progress(by_code("level_3"), fresh) == 0
    assert closest_next(fresh, set()).code == "courses_1"


def test_level_badge_progress_counts_levels_from_two():
    assert progress(by_code("level_3"), Metrics(0, 0, 0, 0, 0, level=2)) == 2
