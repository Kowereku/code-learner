from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from src.model.db import get_db
from src.model.lesson import Lesson
from src.schemas.lesson import LessonDetailRead

router = APIRouter()


@router.get("/{lesson_id}", response_model=LessonDetailRead)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Retrieve lesson details including its list of exercises for the learning view."""
    lesson = (
        db.query(Lesson)
        .options(joinedload(Lesson.exercises))
        .filter(Lesson.id == lesson_id)
        .first()
    )
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson with ID {lesson_id} not found.",
        )
    return lesson
