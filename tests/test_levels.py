from src.core.levels import level_for_xp, xp_for_level


def test_xp_for_level():
    assert [xp_for_level(n) for n in (1, 2, 3, 4, 5, 10)] == [0, 100, 300, 600, 1000, 4500]


def test_level_thresholds():
    assert [level_for_xp(xp) for xp in (0, 99, 100, 299, 300, 4500)] == [1, 1, 2, 2, 3, 10]


def test_level_for_xp_matches_the_curve_at_every_threshold():
    for level in range(1, 60):
        threshold = xp_for_level(level)
        assert level_for_xp(threshold) == level
        assert level_for_xp(threshold - 1) == max(level - 1, 1)
