from datetime import datetime

from pydantic import BaseModel


class CourseCompletionInfo(BaseModel):
    """Info about course completion triggered by finishing its last lesson."""

    course_id: int
    course_name: str
    bonus_xp: int


class LessonCompleteResponse(BaseModel):
    """Response returned after completing a lesson."""

    user_id: int
    lesson_id: int
    xp_earned: int
    total_xp: int
    is_first_completion: bool
    mistakes_made: int
    completed_at: datetime
    course_completed: CourseCompletionInfo | None = None
