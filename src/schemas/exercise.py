from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

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
    options: list[str] | list[list[str]] | None = None

    model_config = ConfigDict(from_attributes=True)


class ChatMessage(BaseModel):
    role: Literal["assistant", "user"]
    content: str = Field(min_length=1, max_length=1000)


class ExerciseChat(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=20)


class ExerciseChatRead(BaseModel):
    passed: bool
    reply: str = Field(min_length=1, max_length=1000)
