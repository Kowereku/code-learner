from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from src.schemas.module import ModuleDetailRead


class CourseBase(BaseModel):
    name: str
    description: str | None = None
    icon_url: str | None = None


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CourseTreeRead(CourseRead):
    modules: list[ModuleDetailRead] = []

    model_config = ConfigDict(from_attributes=True)
