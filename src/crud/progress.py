from datetime import datetime, timezone

from sqlalchemy.orm import Session, selectinload

from src.model.course import Course
from src.model.lesson import Lesson
from src.model.module import Module
from src.model.user import User
from src.model.user_course import UserCourse
from src.model.user_lesson import UserLesson
from src.schemas.reward import CourseCompletionInfo, LessonCompleteResponse


def get_completed_lessons(db: Session, user_id: int) -> list[tuple[int, int]]:
    """Return (lesson_id, course_id) for every lesson the user has completed."""
    return (
        db.query(UserLesson.lesson_id, Module.course_id)
        .join(Lesson, Lesson.id == UserLesson.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .filter(UserLesson.user_id == user_id, UserLesson.completed_at.isnot(None))
        .all()
    )


def _get_course_for_lesson(db: Session, lesson: Lesson) -> Course:
    """Resolve the Course that a lesson belongs to via its module."""
    module = db.query(Module).filter(Module.id == lesson.module_id).first()
    return (
        db.query(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .filter(Course.id == module.course_id)
        .first()
    )


def _get_all_course_lesson_ids(course: Course) -> set[int]:
    """Return a set of all lesson IDs belonging to a course."""
    return {
        lesson.id
        for module in course.modules
        for lesson in module.lessons
    }


def _get_user_completed_lesson_ids(
    db: Session, user_id: int, lesson_ids: set[int]
) -> set[int]:
    """Return the subset of lesson_ids that the user has already completed."""
    if not lesson_ids:
        return set()
    rows = (
        db.query(UserLesson.lesson_id)
        .filter(
            UserLesson.user_id == user_id,
            UserLesson.lesson_id.in_(lesson_ids),
            UserLesson.completed_at.isnot(None),
        )
        .all()
    )
    return {row[0] for row in rows}


def _check_and_complete_course(
    db: Session,
    user: User,
    course: Course,
) -> CourseCompletionInfo | None:
    """If all lessons in the course are completed, mark the course as completed
    and award the course bonus XP.  Returns info about the bonus, or None."""
    all_lesson_ids = _get_all_course_lesson_ids(course)
    completed_ids = _get_user_completed_lesson_ids(db, user.id, all_lesson_ids)

    if completed_ids < all_lesson_ids:
        # Not all lessons completed yet
        return None

    # Check if user is enrolled and not already completed
    user_course = (
        db.query(UserCourse)
        .filter(
            UserCourse.user_id == user.id,
            UserCourse.course_id == course.id,
        )
        .first()
    )
    if user_course is None:
        # User was not enrolled — auto-enroll and mark completed
        user_course = UserCourse(
            user_id=user.id,
            course_id=course.id,
            is_active=True,
        )
        db.add(user_course)

    if user_course.completed:
        # Already completed previously — no duplicate bonus
        return None

    now = datetime.now(timezone.utc)
    user_course.completed = True
    user_course.completed_at = now

    bonus_xp = course.xp_reward
    if bonus_xp > 0:
        user.total_xp += bonus_xp

    return CourseCompletionInfo(
        course_id=course.id,
        course_name=course.name,
        bonus_xp=bonus_xp,
    )


def complete_lesson(
    db: Session,
    user: User,
    lesson: Lesson,
    mistakes_made: int,
) -> LessonCompleteResponse:
    """Mark a lesson completed, award XP on first completion, and check
    whether the entire course has been finished.

    Returns a structured response with all reward details.
    """
    now = datetime.now(timezone.utc)
    is_first_completion = False
    xp_earned = 0

    # Upsert UserLesson row
    user_lesson = db.get(UserLesson, (user.id, lesson.id))
    if user_lesson is None:
        user_lesson = UserLesson(user_id=user.id, lesson_id=lesson.id)
        db.add(user_lesson)

    if user_lesson.completed_at is None:
        # ---- First completion ----
        is_first_completion = True
        xp_earned = lesson.xp_reward
        user.total_xp += xp_earned
        user_lesson.completed_at = now
        user_lesson.mistakes_made = mistakes_made
        user_lesson.status = "completed"
    else:
        # ---- Repeat attempt — update best score only ----
        if mistakes_made < user_lesson.mistakes_made:
            user_lesson.mistakes_made = mistakes_made

    # Flush so that subsequent queries see the new completion
    db.flush()

    # Check course completion
    course = _get_course_for_lesson(db, lesson)
    course_completion: CourseCompletionInfo | None = None
    if course and is_first_completion:
        course_completion = _check_and_complete_course(db, user, course)
        if course_completion and course_completion.bonus_xp > 0:
            xp_earned += course_completion.bonus_xp

    db.commit()
    db.refresh(user)

    return LessonCompleteResponse(
        user_id=user.id,
        lesson_id=lesson.id,
        xp_earned=xp_earned,
        total_xp=user.total_xp,
        is_first_completion=is_first_completion,
        mistakes_made=user_lesson.mistakes_made,
        completed_at=user_lesson.completed_at,
        course_completed=course_completion,
    )
