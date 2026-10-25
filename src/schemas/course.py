from typing import Self

from pydantic import BaseModel, ConfigDict

from src.model.course import Course
from src.model.track import Track
from src.schemas.localized import Localized
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


class CourseListItem(Localized):
    id: int
    name: str
    description: str | None = None
    icon_url: str | None = None
    track: Track | None = None
    xp_reward: int = 0
    modules_count: int = 0
    lessons_count: int = 0

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_course(cls, course: Course, locale: str) -> Self:
        return cls.model_validate(
            {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "icon_url": course.icon_url,
                "track": course.track,
                "xp_reward": course.xp_reward,
                "modules_count": len(course.modules),
                "lessons_count": sum(len(module.lessons) for module in course.modules),
                "translations": course.translations,
            },
            context={"locale": locale},
        )


class CourseDetail(Localized):
    id: int
    name: str
    description: str | None = None
    icon_url: str | None = None
    language: str
    xp_reward: int = 0
    modules: list["ModuleDetailRead"] = []

    model_config = ConfigDict(from_attributes=True)


# Backward-compatibility aliases
CourseRead = CourseListItem
CourseTreeRead = CourseDetail
