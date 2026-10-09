from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.course import CourseRead


class UserCourseBase(BaseModel):
    """Base schema for user course enrollment."""

    course_id: int = Field(..., description="ID of the course to enroll in")


class UserCourseCreate(UserCourseBase):
    """Payload for enrolling the current user in a course."""

    pass


class UserCourseRead(BaseModel):
    """Response representation of a user course enrollment."""

    user_id: int
    course_id: int
    enrolled_at: datetime
    is_active: bool
    course: CourseRead | None = None

    model_config = ConfigDict(from_attributes=True)
