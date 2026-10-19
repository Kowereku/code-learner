from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.deps import get_current_user, get_locale
from src.crud import lesson as lesson_crud
from src.crud import progress as progress_crud
from src.model.db import get_db
from src.model.user import User
from src.schemas.lesson import LessonComplete, LessonDetailRead
from src.schemas.reward import LessonCompleteResponse

router = APIRouter()


@router.get("/{lesson_id}", response_model=LessonDetailRead)
def get_lesson(
    lesson_id: int, db: Session = Depends(get_db), locale: str = Depends(get_locale)
) -> LessonDetailRead:
    """Retrieve lesson details including its list of exercises for the learning view."""
    lesson = lesson_crud.get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson with ID {lesson_id} not found.",
        )
    return LessonDetailRead.model_validate(lesson, context={"locale": locale})


@router.post("/{lesson_id}/complete", response_model=LessonCompleteResponse)
def complete_lesson(
    lesson_id: int,
    lesson_in: LessonComplete,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LessonCompleteResponse:
    """Mark a lesson as completed by the current user.

    On first completion the user receives the lesson's full XP reward.
    Repeat completions award 0 XP but may update the best-mistakes score.
    If this was the last lesson in a course, the course is automatically
    marked as completed and the course bonus XP is awarded.
    """
    lesson = lesson_crud.get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson with ID {lesson_id} not found.",
        )
    return progress_crud.complete_lesson(
        db, current_user, lesson, lesson_in.mistakes_made
    )
