from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from src.schemas.module import ModuleResponse


class CourseBase(BaseModel):
    name: str
    description: str | None = None
    icon_url: str | None = None


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    modules: list[ModuleResponse] = []

    model_config = ConfigDict(from_attributes=True)


# Backward compatibility aliases
CourseRead = CourseResponse
CourseTreeRead = CourseResponse
