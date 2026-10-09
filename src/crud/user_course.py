from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload

from src.model.course import Course
from src.model.user import User
from src.model.user_course import UserCourse


def get_user_courses(
    db: Session, user_id: int, active_only: bool = True
) -> list[UserCourse]:
    """Retrieve all courses enrolled by the given user.

    Uses selectinload to eagerly load the associated Course entity,
    preventing N+1 query performance issues.
    """
    query = (
        db.query(UserCourse)
        .options(selectinload(UserCourse.course))
        .filter(UserCourse.user_id == user_id)
    )
    if active_only:
        query = query.filter(UserCourse.is_active.is_(True))
    return query.all()


def get_user_course(
    db: Session, user_id: int, course_id: int
) -> UserCourse | None:
    """Retrieve a single user-course link by user_id and course_id."""
    return (
        db.query(UserCourse)
        .options(selectinload(UserCourse.course))
        .filter(UserCourse.user_id == user_id, UserCourse.course_id == course_id)
        .first()
    )


def enroll_user_in_course(
    db: Session, user_id: int, course_id: int
) -> UserCourse:
    """Enroll a user in a specific course.

    Checks whether the course and user exist, and raises HTTP 400 if the user
    is already actively enrolled in the course.
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found.",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )

    user_course = (
        db.query(UserCourse)
        .filter(UserCourse.user_id == user_id, UserCourse.course_id == course_id)
        .first()
    )

    if user_course:
        if user_course.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already enrolled in this course.",
            )
        # Reactivate inactive enrollment
        user_course.is_active = True
        user_course.enrolled_at = datetime.now(timezone.utc)
        db.commit()
    else:
        user_course = UserCourse(
            user_id=user_id,
            course_id=course_id,
            is_active=True,
        )
        db.add(user_course)
        db.commit()

    # Re-fetch with eager loaded course relationship to ensure clean serialization
    return (
        db.query(UserCourse)
        .options(selectinload(UserCourse.course))
        .filter(UserCourse.user_id == user_id, UserCourse.course_id == course_id)
        .first()
    )


def disenroll_user_from_course(
    db: Session, user_id: int, course_id: int
) -> bool:
    """Remove a user's enrollment from a course."""
    user_course = (
        db.query(UserCourse)
        .filter(UserCourse.user_id == user_id, UserCourse.course_id == course_id)
        .first()
    )
    if not user_course:
        return False
    db.delete(user_course)
    db.commit()
    return True
