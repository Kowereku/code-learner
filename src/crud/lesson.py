from sqlalchemy.orm import Session, joinedload

from src.model.lesson import Lesson


def get_lesson_by_id(db: Session, lesson_id: int) -> Lesson | None:
    """Retrieve a lesson by ID along with its associated exercises."""
    return (
        db.query(Lesson)
        .options(joinedload(Lesson.exercises))
        .filter(Lesson.id == lesson_id)
        .first()
    )
