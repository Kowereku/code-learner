"""Badge definitions and progress rules.

Badges are defined here, not in the database; their names and descriptions live in the
frontend locale files, keyed by code. Every badge counts towards a goal on one metric.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Metrics:
    """Per-user numbers the badges are measured on."""

    courses_completed: int
    best_streak: int
    flawless_lessons: int
    perfect_quizzes: int
    code_answers: int
    current_streak: int = 0
    level: int = 0

    @property
    def level_progress(self) -> int:
        """Progress towards level badges: level 1 is where everyone starts, so it counts as 0."""
        return self.level if self.level > 1 else 0


@dataclass(frozen=True)
class BadgeDef:
    """One badge: reached when the named Metrics field hits the goal.

    progress_metric, when set, is what an unearned badge shows progress on. Streak badges
    are awarded on the best streak, so they stay earned after a break, but a new attempt
    starts from the current streak.
    """

    code: str
    family: str
    goal: int
    metric: str
    progress_metric: str | None = None


BADGES: list[BadgeDef] = [
    BadgeDef("courses_1", "courses", 1, "courses_completed"),
    BadgeDef("courses_5", "courses", 5, "courses_completed"),
    BadgeDef("courses_10", "courses", 10, "courses_completed"),
    BadgeDef("streak_3", "streak", 3, "best_streak", "current_streak"),
    BadgeDef("streak_5", "streak", 5, "best_streak", "current_streak"),
    BadgeDef("streak_10", "streak", 10, "best_streak", "current_streak"),
    BadgeDef("streak_30", "streak", 30, "best_streak", "current_streak"),
    BadgeDef("flawless_lesson", "flawless_lesson", 1, "flawless_lessons"),
    BadgeDef("perfect_quiz", "perfect_quiz", 1, "perfect_quizzes"),
    BadgeDef("own_code_10", "own_code", 10, "code_answers"),
    BadgeDef("own_code_50", "own_code", 50, "code_answers"),
    BadgeDef("own_code_100", "own_code", 100, "code_answers"),
    BadgeDef("level_3", "level", 3, "level", "level_progress"),
    BadgeDef("level_5", "level", 5, "level", "level_progress"),
    BadgeDef("level_10", "level", 10, "level", "level_progress"),
]


def _reached(badge: BadgeDef, metrics: Metrics) -> bool:
    return getattr(metrics, badge.metric) >= badge.goal


def progress(badge: BadgeDef, metrics: Metrics) -> int:
    """Return how far the user got towards the badge: the goal once reached, else capped below it."""
    if _reached(badge, metrics):
        return badge.goal
    return min(getattr(metrics, badge.progress_metric or badge.metric), badge.goal)


def earned_codes(metrics: Metrics) -> set[str]:
    """Return the codes of every badge whose goal is reached."""
    return {badge.code for badge in BADGES if _reached(badge, metrics)}


def closest_next(metrics: Metrics, earned: set[str]) -> BadgeDef | None:
    """Return the unearned badge with the highest share done; ties go to the smaller goal."""
    remaining = [(index, badge) for index, badge in enumerate(BADGES) if badge.code not in earned]
    if not remaining:
        return None
    _, best = min(
        remaining,
        key=lambda item: (-progress(item[1], metrics) / item[1].goal, item[1].goal, item[0]),
    )
    return best
