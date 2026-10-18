from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.model.user_lesson import UserLesson
from src.schemas.user_progress import UserProgressUpdate


def get_user_progress(
    db: Session,
    user_id: int,
    lesson_id: int,
) -> UserLesson | None:
    """Retrieve current user progress for a specific lesson."""
    return (
        db.query(UserLesson)
        .filter(
            UserLesson.user_id == user_id,
            UserLesson.lesson_id == lesson_id,
        )
        .first()
    )


def upsert_user_progress(
    db: Session,
    user_id: int,
    lesson_id: int,
    progress_in: UserProgressUpdate,
) -> UserLesson:
    """Update existing user progress or create a new row if none exists."""
    progress = get_user_progress(db, user_id=user_id, lesson_id=lesson_id)
    update_data = progress_in.model_dump(exclude_unset=True)

    if progress:
        if "status" in update_data and update_data["status"] is not None:
            progress.status = update_data["status"]
        if "last_position" in update_data:
            progress.last_position = update_data["last_position"]
        progress.updated_at = datetime.now(timezone.utc)
    else:
        status_val = update_data.get("status") or "in_progress"
        progress = UserLesson(
            user_id=user_id,
            lesson_id=lesson_id,
            status=status_val,
            last_position=update_data.get("last_position"),
        )
        db.add(progress)

    db.commit()
    db.refresh(progress)
    return progress
