from datetime import date, datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from src.core.badges import BADGES, BadgeDef, Metrics, earned_codes, progress
from src.core.levels import level_for_xp
from src.core.streak import displayed_streak
from src.model.lesson import Lesson
from src.model.module import Module
from src.model.user import User
from src.model.user_badge import UserBadge
from src.model.user_code_solution import UserCodeSolution
from src.model.user_lesson import UserLesson
from src.schemas.badge import BadgeRead


def _courses_completed(db: Session, user_id: int) -> int:
    """Count courses whose every lesson the user has completed.

    Counted from lessons, like the profile does, so the stat and the course badges agree
    even for courses finished before courses were marked completed automatically.
    """
    finished = (
        select(Module.course_id)
        .join(Lesson, Lesson.module_id == Module.id)
        .outerjoin(
            UserLesson,
            (UserLesson.lesson_id == Lesson.id)
            & (UserLesson.user_id == user_id)
            & UserLesson.completed_at.isnot(None),
        )
        .group_by(Module.course_id)
        .having(func.count(Lesson.id) == func.count(UserLesson.lesson_id))
        .subquery()
    )
    return db.scalar(select(func.count()).select_from(finished))


def get_metrics(db: Session, user: User, today: date) -> Metrics:
    """Compute the numbers the badges are measured on for one user, as of today in their time zone."""
    courses_completed = _courses_completed(db, user.id)
    code_answers = db.scalar(
        select(func.count()).select_from(UserCodeSolution).where(UserCodeSolution.user_id == user.id)
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
        code_answers=code_answers,
        current_streak=displayed_streak(user.last_activity_date, today, user.streak_days),
        level=level_for_xp(user.total_xp),
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


def award_badges(db: Session, user_id: int, codes: list[str], awarded_at: datetime) -> list[str]:
    """Insert the badges, skipping any the user already has, and return the codes actually added.

    ON CONFLICT DO NOTHING keeps two racing lesson completions (e.g. in two tabs) from failing
    on the primary key.
    """
    if not codes:
        return []
    statement = (
        insert(UserBadge)
        .values([{"user_id": user_id, "badge_code": code, "awarded_at": awarded_at} for code in codes])
        .on_conflict_do_nothing()
        .returning(UserBadge.badge_code)
    )
    inserted = set(db.scalars(statement))
    return [code for code in codes if code in inserted]


def record_code_solutions(db: Session, user_id: int, lesson: Lesson, exercise_ids: list[int]) -> None:
    """Remember the lesson's code exercises the user solved by typing; each counts once, ever."""
    code_ids = {exercise.id for exercise in lesson.exercises if exercise.type == "code"}
    solved = sorted(code_ids & set(exercise_ids))
    if not solved:
        return
    db.execute(
        insert(UserCodeSolution)
        .values([{"user_id": user_id, "exercise_id": exercise_id} for exercise_id in solved])
        .on_conflict_do_nothing()
    )


def sync_badges(db: Session, user: User, today: date) -> list[BadgeRead]:
    """Award every badge the user qualifies for but doesn't have yet.

    Runs only when a lesson is completed, inside its transaction (no commit here); reads never award.
    Returns only the newly awarded badges.
    """
    # The app's sessions don't autoflush, so pending progress must be visible to the metric queries.
    db.flush()
    metrics = get_metrics(db, user, today)
    have = _awarded_at(db, user)
    reached = earned_codes(metrics)
    now = datetime.now(timezone.utc)
    missing = [badge.code for badge in BADGES if badge.code in reached and badge.code not in have]
    added = set(award_badges(db, user.id, missing, now))
    return [_read(badge, metrics, now) for badge in BADGES if badge.code in added]


def list_badges(db: Session, user: User, metrics: Metrics) -> list[BadgeRead]:
    """Return all badges in definition order with the user's progress and award dates."""
    awarded = _awarded_at(db, user)
    return [_read(badge, metrics, awarded.get(badge.code)) for badge in BADGES]
