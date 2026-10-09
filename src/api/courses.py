from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.crud import course as course_crud
from src.model.db import get_db
from src.schemas.course import CourseCreate, CourseDetail, CourseListItem

router = APIRouter()


@router.get("", response_model=list[CourseListItem])
def list_courses(
    skip: int = Query(default=0, ge=0, description="Number of courses to skip"),
    limit: int = Query(default=100, ge=1, le=100, description="Max number of courses to return"),
    db: Session = Depends(get_db),
):
    """Retrieve all available courses."""
    return course_crud.get_courses(db, skip=skip, limit=limit)


@router.post("", response_model=CourseListItem, status_code=status.HTTP_201_CREATED)
def create_course(course_in: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course."""
    return course_crud.create_course(db, course_in)


@router.get("/{course_id}", response_model=CourseDetail)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Retrieve course details by ID including modules and lessons."""
    course = course_crud.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found.",
        )
    return course


@router.get("/{course_id}/tree", response_model=CourseDetail)
def get_course_tree(course_id: int, db: Session = Depends(get_db)):
    """Retrieve course with its full learning hierarchy (modules and lessons)."""
    return get_course(course_id=course_id, db=db)
