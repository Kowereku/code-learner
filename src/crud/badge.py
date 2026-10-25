from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.core.badges import BADGES, BadgeDef, Metrics, earned_codes, progress
from src.model.lesson import Lesson
from src.model.user import User
from src.model.user_badge import UserBadge
from src.model.user_course import UserCourse
from src.model.user_lesson import UserLesson
from src.schemas.badge import BadgeRead


def get_metrics(db: Session, user: User) -> Metrics:
    """Compute the numbers the badges are measured on for one user."""
    courses_completed = (
        db.query(func.count())
        .select_from(UserCourse)
        .filter(UserCourse.user_id == user.id, UserCourse.completed.is_(True))
        .scalar()
    )
    flawless_by_quiz = dict(
        db.query(Lesson.is_quiz, func.count())
        .join(UserLesson, UserLesson.lesson_id == Lesson.id)
        .filter(
            UserLesson.user_id == user.id,
            UserLesson.completed_at.isnot(None),
            UserLesson.mistakes_made == 0,
        )
        .group_by(Lesson.is_quiz)
        .all()
    )
    return Metrics(
        courses_completed=courses_completed,
        best_streak=user.best_streak,
        flawless_lessons=flawless_by_quiz.get(False, 0),
        perfect_quizzes=flawless_by_quiz.get(True, 0),
        code_answers=user.code_answers,
        current_streak=user.streak_days,
    )


def _awarded_at(db: Session, user: User) -> dict[str, datetime]:
    """Return when each earned badge was awarded, keyed by badge code."""
    rows = db.query(UserBadge.badge_code, UserBadge.awarded_at).filter(UserBadge.user_id == user.id)
    return dict(rows.all())


def _read(badge: BadgeDef, metrics: Metrics, awarded_at: datetime | None) -> BadgeRead:
    return BadgeRead(
        code=badge.code,
        family=badge.family,
        goal=badge.goal,
        progress=progress(badge, metrics),
        awarded_at=awarded_at,
    )


def sync_badges(db: Session, user: User) -> list[BadgeRead]:
    """Award every badge the user qualifies for but doesn't have yet.

    Flushes but doesn't commit, so it can run inside the lesson-completion transaction.
    Returns only the newly awarded badges.
    """
    # The app's sessions don't autoflush, so pending progress must be visible to the metric queries.
    db.flush()
    metrics = get_metrics(db, user)
    have = _awarded_at(db, user)
    reached = earned_codes(metrics)
    now = datetime.now(timezone.utc)
    new_badges = []
    for badge in BADGES:
        if badge.code in reached and badge.code not in have:
            db.add(UserBadge(user_id=user.id, badge_code=badge.code, awarded_at=now))
            new_badges.append(_read(badge, metrics, now))
    db.flush()
    return new_badges


def list_badges(db: Session, user: User) -> list[BadgeRead]:
    """Return all badges in definition order with the user's progress and award dates."""
    metrics = get_metrics(db, user)
    awarded = _awarded_at(db, user)
    return [_read(badge, metrics, awarded.get(badge.code)) for badge in BADGES]
