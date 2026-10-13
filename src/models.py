"""Re-export models for compatibility with src.models import style."""
from src.model import (
    Base,
    Course,
    Exercise,
    ExerciseType,
    Lesson,
    Module,
    User,
    UserCourse,
    UserLesson,
    UserProgress,
)

__all__ = [
    "Base",
    "Course",
    "Exercise",
    "ExerciseType",
    "Lesson",
    "Module",
    "User",
    "UserCourse",
    "UserLesson",
    "UserProgress",
]
