from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from src.schemas.lesson import LessonRead


class ModuleBase(BaseModel):
    title: str
    order_index: int


class ModuleCreate(ModuleBase):
    pass


class ModuleRead(ModuleBase):
    id: int
    course_id: int

    model_config = ConfigDict(from_attributes=True)


class ModuleDetailRead(ModuleRead):
    lessons: list[LessonRead] = []

    model_config = ConfigDict(from_attributes=True)
