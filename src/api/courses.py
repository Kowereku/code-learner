from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.crud import course as course_crud
from src.model.db import get_db
from src.schemas.course import CourseCreate, CourseRead, CourseTreeRead

router = APIRouter()


@router.get("", response_model=list[CourseRead])
def list_courses(db: Session = Depends(get_db)):
    """Retrieve all available courses."""
    return course_crud.get_courses(db)


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(course_in: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course."""
    return course_crud.create_course(db, course_in)


@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Retrieve course details by ID."""
    course = course_crud.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found.",
        )
    return course


@router.get("/{course_id}/tree", response_model=CourseTreeRead)
def get_course_tree(course_id: int, db: Session = Depends(get_db)):
    """Retrieve course with its full learning hierarchy (modules and lessons)."""
    course = course_crud.get_course_tree(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found.",
        )
    return course
