from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.model.lesson import Lesson
from src.model.module import Module
from src.model.user import User
from src.model.user_lesson import UserLesson


def get_completed_lessons(db: Session, user_id: int) -> list[tuple[int, int]]:
    """Return (lesson_id, course_id) for every lesson the user has completed."""
    return (
        db.query(UserLesson.lesson_id, Module.course_id)
        .join(Lesson, Lesson.id == UserLesson.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .filter(UserLesson.user_id == user_id, UserLesson.completed_at.isnot(None))
        .all()
    )


def complete_lesson(db: Session, user: User, lesson: Lesson, mistakes_made: int) -> User:
    """Mark a lesson completed; XP is awarded only on the first completion."""
    user_lesson = db.get(UserLesson, (user.id, lesson.id))
    if user_lesson is None:
        user_lesson = UserLesson(user_id=user.id, lesson_id=lesson.id)
        db.add(user_lesson)
    if user_lesson.completed_at is None:
        user.total_xp += lesson.xp_reward
    user_lesson.completed_at = datetime.now(timezone.utc)
    user_lesson.mistakes_made = mistakes_made
    db.commit()
    db.refresh(user)
    return user
