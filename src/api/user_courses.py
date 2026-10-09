from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.crud import user_course as user_course_crud
from src.model.db import get_db
from src.model.user import User
from src.schemas.user_course import UserCourseCreate, UserCourseRead

router = APIRouter()


@router.post(
    "/me/courses",
    response_model=UserCourseRead,
    status_code=status.HTTP_201_CREATED,
    summary="Enroll current user in a course",
)
def enroll_current_user_in_course(
    enroll_data: UserCourseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Enroll the currently authenticated user in a specified course."""
    return user_course_crud.enroll_user_in_course(
        db, user_id=current_user.id, course_id=enroll_data.course_id
    )


@router.get(
    "/me/courses",
    response_model=list[UserCourseRead],
    summary="Get enrolled courses for current user",
)
def get_current_user_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve all courses enrolled by the currently authenticated user."""
    return user_course_crud.get_user_courses(db, user_id=current_user.id)
