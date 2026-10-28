"""Level curve: levels are a visual reward derived from total XP, never stored."""

from math import isqrt


def xp_for_level(level: int) -> int:
    """Total XP needed to reach a level: 0, 100, 300, 600, 1000, ... (each level costs 100 more)."""
    return 50 * level * (level - 1)


def level_for_xp(xp: int) -> int:
    """Return the highest level whose XP threshold has been reached.

    Solves 50·n·(n − 1) ≤ xp for n with integer maths, then corrects the rounding.
    """
    level = max(1, (1 + isqrt(1 + (2 * max(xp, 0)) // 25)) // 2)
    while xp_for_level(level + 1) <= xp:
        level += 1
    while level > 1 and xp_for_level(level) > xp:
        level -= 1
    return level
