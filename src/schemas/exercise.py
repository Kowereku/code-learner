from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ExerciseBase(BaseModel):
    type: str
    content: str
    code_snippet: str | None = None
    correct_answer: str


class ExerciseCreate(ExerciseBase):
    lesson_id: int | None = None


class ExerciseResponse(ExerciseBase):
    id: int
    lesson_id: int

    model_config = ConfigDict(from_attributes=True)


# Backward compatibility alias
ExerciseRead = ExerciseResponse
