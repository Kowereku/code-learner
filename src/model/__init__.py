"""SQLAlchemy models package.

Importing the package registers every model on ``Base.metadata`` so that
Alembic autogenerate can detect the full schema.
"""

from src.model.db import Base
from src.model.course import Course
from src.model.exercise import Exercise, ExerciseType
from src.model.lesson import Lesson
from src.model.module import Module
from src.model.user import User
from src.model.user_course import UserCourse
from src.model.user_lesson import UserLesson

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
]
