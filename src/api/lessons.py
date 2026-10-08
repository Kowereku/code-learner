from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.crud import lesson as lesson_crud
from src.crud import progress as progress_crud
from src.model.db import get_db
from src.model.user import User
from src.schemas.lesson import LessonComplete, LessonDetailRead
from src.schemas.user import UserRead

router = APIRouter()


@router.get("/{lesson_id}", response_model=LessonDetailRead)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Retrieve lesson details including its list of exercises for the learning view."""
    lesson = lesson_crud.get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson with ID {lesson_id} not found.",
        )
    return lesson


@router.post("/{lesson_id}/complete", response_model=UserRead)
def complete_lesson(
    lesson_id: int,
    lesson_in: LessonComplete,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a lesson as completed by the current user, awarding XP on the first completion."""
    lesson = lesson_crud.get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson with ID {lesson_id} not found.",
        )
    return progress_crud.complete_lesson(db, current_user, lesson, lesson_in.mistakes_made)
