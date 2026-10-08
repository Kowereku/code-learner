from __future__ import annotations

from sqlalchemy.orm import Session, selectinload

from src.model.course import Course
from src.model.module import Module
from src.schemas.course import CourseCreate


def get_courses(db: Session, skip: int = 0, limit: int = 100) -> list[Course]:
    """Retrieve all available courses from the database with pagination."""
    return (
        db.query(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_course_by_id(db: Session, course_id: int) -> Course | None:
    """Retrieve a single course by its ID with modules and lessons eagerly loaded."""
    course = (
        db.query(Course)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
        .filter(Course.id == course_id)
        .first()
    )
    if course:
        course.modules.sort(key=lambda m: m.order_index)
    return course


def create_course(db: Session, course_in: CourseCreate) -> Course:
    """Create and persist a new course."""
    course = Course(
        name=course_in.name,
        description=course_in.description,
        icon_url=course_in.icon_url,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_course_tree(db: Session, course_id: int) -> Course | None:
    """Retrieve a course with all nested modules and lessons loaded and ordered."""
    return get_course_by_id(db, course_id)
