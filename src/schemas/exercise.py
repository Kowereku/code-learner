from pydantic import BaseModel, ConfigDict

from src.model.exercise import ExerciseType


class ExerciseBase(BaseModel):
    type: ExerciseType
    content: str
    code_snippet: str | None = None
    correct_answer: str


class ExerciseCreate(BaseModel):
    type: ExerciseType
    content: str
    code_snippet: str | None = None
    correct_answer: str


class ExerciseRead(BaseModel):
    id: int
    lesson_id: int
    type: ExerciseType
    content: str
    code_snippet: str | None = None
    correct_answer: str

    model_config = ConfigDict(from_attributes=True)
