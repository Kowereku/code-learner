from sqlalchemy.orm import Session, joinedload

from src.model.course import Course
from src.model.module import Module
from src.schemas.course import CourseCreate


def get_courses(db: Session) -> list[Course]:
    """Retrieve all available courses from the database."""
    return db.query(Course).all()


def get_course_by_id(db: Session, course_id: int) -> Course | None:
    """Retrieve a single course by its ID."""
    return db.query(Course).filter(Course.id == course_id).first()


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
    course = (
        db.query(Course)
        .options(joinedload(Course.modules).joinedload(Module.lessons))
        .filter(Course.id == course_id)
        .first()
    )
    if course:
        course.modules.sort(key=lambda m: m.order_index)
    return course
