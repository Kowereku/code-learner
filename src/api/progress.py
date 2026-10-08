from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.crud import progress as progress_crud
from src.model.db import get_db
from src.model.user import User
from src.schemas.progress import ProgressRead

router = APIRouter()


@router.get("", response_model=ProgressRead)
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve the lessons completed by the current user."""
    rows = progress_crud.get_completed_lessons(db, current_user.id)
    return {
        "completed_lessons": [
            {"lesson_id": lesson_id, "course_id": course_id} for lesson_id, course_id in rows
        ]
    }
