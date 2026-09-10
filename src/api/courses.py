from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from src.model.course import Course
from src.model.db import get_db
from src.schemas.course import CourseCreate, CourseRead, CourseTreeRead

router = APIRouter()


@router.get("", response_model=list[CourseRead])
def list_courses(db: Session = Depends(get_db)):
    """Retrieve all available courses."""
    return db.query(Course).all()


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(course_in: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course."""
    course = Course(
        name=course_in.name,
        description=course_in.description,
        icon_url=course_in.icon_url,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Retrieve course details by ID."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found.",
        )
    return course


@router.get("/{course_id}/tree", response_model=CourseTreeRead)
def get_course_tree(course_id: int, db: Session = Depends(get_db)):
    """Retrieve course with its full learning hierarchy (modules and lessons)."""
    course = (
        db.query(Course)
        .options(joinedload(Course.modules).joinedload(Course.modules.property.mapper.class_.lessons))
        .filter(Course.id == course_id)
        .first()
    )
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found.",
        )
    # Sort modules by order_index for consistent curriculum display
    course.modules.sort(key=lambda m: m.order_index)
    return course
