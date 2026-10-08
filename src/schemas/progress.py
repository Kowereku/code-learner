from pydantic import BaseModel


class CompletedLessonRead(BaseModel):
    lesson_id: int
    course_id: int


class ProgressRead(BaseModel):
    completed_lessons: list[CompletedLessonRead] = []
