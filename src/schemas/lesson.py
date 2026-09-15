from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.exercise import ExerciseResponse


class LessonBase(BaseModel):
    title: str
    xp_reward: int = 0


class LessonCreate(LessonBase):
    module_id: int | None = None


class LessonResponse(LessonBase):
    id: int
    module_id: int
    exercises: list[ExerciseResponse] = []

    model_config = ConfigDict(from_attributes=True)


# Backward compatibility aliases
LessonRead = LessonResponse
LessonDetailRead = LessonResponse
