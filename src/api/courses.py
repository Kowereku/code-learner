from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.api.deps import get_current_user, get_locale
from src.crud import course as course_crud
from src.crud import user_course as user_course_crud
from src.model.db import get_db
from src.model.user import User
from src.schemas.course import CourseCreate, CourseDetail, CourseListItem
from src.schemas.user_course import UserCourseRead

router = APIRouter()


@router.get("", response_model=list[CourseListItem])
def list_courses(
    skip: int = Query(default=0, ge=0, description="Number of courses to skip"),
    limit: int = Query(default=100, ge=1, le=100, description="Max number of courses to return"),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale),
) -> list[CourseListItem]:
    """Retrieve all available courses."""
    courses = course_crud.get_courses(db, skip=skip, limit=limit)
    return [CourseListItem.from_course(course, locale) for course in courses]


@router.post("", response_model=CourseListItem, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale),
) -> CourseListItem:
    """Create a new course."""
    return CourseListItem.from_course(course_crud.create_course(db, course_in), locale)


@router.get("/{course_id}", response_model=CourseDetail)
def get_course(
    course_id: int, db: Session = Depends(get_db), locale: str = Depends(get_locale)
) -> CourseDetail:
    """Retrieve course details by ID including modules and lessons."""
    course = course_crud.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found.",
        )
    return CourseDetail.model_validate(course, context={"locale": locale})


@router.get("/{course_id}/tree", response_model=CourseDetail)
def get_course_tree(
    course_id: int, db: Session = Depends(get_db), locale: str = Depends(get_locale)
) -> CourseDetail:
    """Retrieve course with its full learning hierarchy (modules and lessons)."""
    return get_course(course_id=course_id, db=db, locale=locale)


@router.post(
    "/{course_id}/enroll",
    response_model=UserCourseRead,
    status_code=status.HTTP_201_CREATED,
    summary="Enroll current user in course by ID",
)
def enroll_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Enroll the currently authenticated user in the specified course."""
    return user_course_crud.enroll_user_in_course(
        db, user_id=current_user.id, course_id=course_id
    )
