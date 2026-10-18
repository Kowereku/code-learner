from typing import Self

from pydantic import BaseModel, ConfigDict

from src.model.course import Course
from src.schemas.module import ModuleDetailRead


class CourseBase(BaseModel):
    name: str
    description: str | None = None
    icon_url: str | None = None


class CourseCreate(BaseModel):
    name: str
    description: str | None = None
    icon_url: str | None = None
    language: str


class CourseListItem(BaseModel):
    id: int
    name: str
    description: str | None = None
    icon_url: str | None = None
    modules_count: int = 0
    lessons_count: int = 0

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_course(cls, course: Course) -> Self:
        return cls(
            id=course.id,
            name=course.name,
            description=course.description,
            icon_url=course.icon_url,
            modules_count=len(course.modules),
            lessons_count=sum(len(module.lessons) for module in course.modules),
        )


class CourseDetail(BaseModel):
    id: int
    name: str
    description: str | None = None
    icon_url: str | None = None
    language: str
    modules: list["ModuleDetailRead"] = []

    model_config = ConfigDict(from_attributes=True)
