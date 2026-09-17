from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.crud import lesson as lesson_crud
from src.model.db import get_db
from src.schemas.lesson import LessonDetailRead

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
