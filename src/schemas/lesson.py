from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from src.schemas.exercise import ExerciseRead


class LessonBase(BaseModel):
    title: str
    xp_reward: int = 0


class LessonCreate(LessonBase):
    pass


class LessonRead(LessonBase):
    id: int
    module_id: int

    model_config = ConfigDict(from_attributes=True)


class LessonDetailRead(LessonRead):
    exercises: list[ExerciseRead] = []

    model_config = ConfigDict(from_attributes=True)
