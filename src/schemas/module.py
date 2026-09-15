from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.lesson import LessonResponse


class ModuleBase(BaseModel):
    title: str
    order_index: int


class ModuleCreate(ModuleBase):
    course_id: int | None = None


class ModuleResponse(ModuleBase):
    id: int
    course_id: int
    lessons: list[LessonResponse] = []

    model_config = ConfigDict(from_attributes=True)


# Backward compatibility aliases
ModuleRead = ModuleResponse
ModuleDetailRead = ModuleResponse
