from pydantic import BaseModel

from src.schemas.course import CourseListItem
from src.schemas.user import UserRead


class ProfileStats(BaseModel):
    """Numbers shown in the profile's user card."""

    total_xp: int
    streak_days: int
    courses_completed: int


class NextLessonRead(BaseModel):
    """The first lesson of a course the user hasn't completed yet."""

    id: int
    title: str
    module_title: str


class ProfileCourse(BaseModel):
    """A course the user has started, with how far they got."""

    course: CourseListItem
    completed_lessons: int
    completed: bool
    next_lesson: NextLessonRead | None = None


class ProfileRead(BaseModel):
    """Everything the profile page shows, in one response."""

    user: UserRead
    stats: ProfileStats
    courses: list[ProfileCourse] = []
    suggested_course: CourseListItem | None = None
