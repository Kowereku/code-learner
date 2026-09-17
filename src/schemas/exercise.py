from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from src.model.exercise import ExerciseType


class ExerciseBase(BaseModel):
    type: ExerciseType
    content: str
    code_snippet: str | None = None
    correct_answer: str


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseRead(ExerciseBase):
    id: int
    lesson_id: int

    model_config = ConfigDict(from_attributes=True)
