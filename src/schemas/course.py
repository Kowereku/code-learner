from pydantic import BaseModel, ConfigDict

from src.schemas.module import ModuleDetailRead


class CourseBase(BaseModel):
    name: str
    description: str | None = None
    icon_url: str | None = None


class CourseCreate(BaseModel):
    name: str
    description: str | None = None
    icon_url: str | None = None


class CourseRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    icon_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CourseTreeRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    icon_url: str | None = None
    modules: list[ModuleDetailRead] = []

    model_config = ConfigDict(from_attributes=True)
