from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.crud import lesson as lesson_crud
from src.crud import progress as progress_crud
from src.crud import user_progress as user_progress_crud
from src.model.db import get_db
from src.model.user import User
from src.schemas.progress import CompletedLessonRead, ProgressRead
from src.schemas.user_progress import UserProgressRead, UserProgressUpdate

router = APIRouter()


@router.put(
    "/users/me/lessons/{lesson_id}/progress",
    response_model=UserProgressRead,
    summary="Save user lesson progress",
)
def save_user_lesson_progress(
    lesson_id: int,
    progress_in: UserProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Save or update the exact progress/state where the user paused a lesson."""
    lesson = lesson_crud.get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson with ID {lesson_id} not found.",
        )

    return user_progress_crud.upsert_user_progress(
        db=db,
        user_id=current_user.id,
        lesson_id=lesson_id,
        progress_in=progress_in,
    )


@router.get(
    "/users/me/lessons/{lesson_id}/progress",
    response_model=UserProgressRead,
    summary="Get user lesson progress",
)
def get_user_lesson_progress(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve the saved progress/state of the current user for a specific lesson."""
    lesson = lesson_crud.get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson with ID {lesson_id} not found.",
        )

    progress = user_progress_crud.get_user_progress(
        db=db,
        user_id=current_user.id,
        lesson_id=lesson_id,
    )
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Progress for lesson {lesson_id} not found.",
        )

    return progress


@router.get("", response_model=ProgressRead)
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProgressRead:
    """Retrieve the lessons completed by the current user."""
    rows = progress_crud.get_completed_lessons(db, current_user.id)
    return ProgressRead(
        completed_lessons=[
            CompletedLessonRead(lesson_id=lesson_id, course_id=course_id)
            for lesson_id, course_id in rows
        ]
    )