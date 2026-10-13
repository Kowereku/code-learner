"""Pydantic schemas package."""
from src.schemas.auth import LoginData, Token, TokenPayload
from src.schemas.course import CourseBase, CourseCreate, CourseRead, CourseTreeRead
from src.schemas.exercise import ExerciseBase, ExerciseCreate, ExerciseRead
from src.schemas.lesson import (
    LessonBase,
    LessonCreate,
    LessonDetailRead,
    LessonRead,
)
from src.schemas.module import (
    ModuleBase,
    ModuleCreate,
    ModuleDetailRead,
    ModuleRead,
)
from src.schemas.user import UserBase, UserCreate, UserRead
from src.schemas.user_progress import UserProgressRead, UserProgressUpdate

# Backward-compatibility aliases
CourseResponse = CourseRead
ExerciseResponse = ExerciseRead
LessonResponse = LessonRead
ModuleResponse = ModuleRead

__all__ = [
    "CourseBase",
    "CourseCreate",
    "CourseRead",
    "CourseResponse",
    "CourseTreeRead",
    "ExerciseBase",
    "ExerciseCreate",
    "ExerciseRead",
    "ExerciseResponse",
    "LessonBase",
    "LessonCreate",
    "LessonDetailRead",
    "LessonRead",
    "LessonResponse",
    "LoginData",
    "ModuleBase",
    "ModuleCreate",
    "ModuleDetailRead",
    "ModuleRead",
    "ModuleResponse",
    "Token",
    "TokenPayload",
    "UserBase",
    "UserCreate",
    "UserRead",
    "UserProgressUpdate",
    "UserProgressRead",
]
