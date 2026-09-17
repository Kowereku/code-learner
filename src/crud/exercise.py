from sqlalchemy.orm import Session

from src.model.exercise import Exercise


def get_exercise_by_id(db: Session, exercise_id: int) -> Exercise | None:
    """Retrieve an exercise by its ID."""
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()
