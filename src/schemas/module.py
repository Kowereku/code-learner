from pydantic import BaseModel, ConfigDict

from src.schemas.lesson import LessonRead


class ModuleBase(BaseModel):
    title: str
    order_index: int


class ModuleCreate(BaseModel):
    title: str
    order_index: int


class ModuleRead(BaseModel):
    id: int
    course_id: int
    title: str
    order_index: int

    model_config = ConfigDict(from_attributes=True)


class ModuleDetailRead(BaseModel):
    id: int
    course_id: int
    title: str
    order_index: int
    lessons: list[LessonRead] = []

    model_config = ConfigDict(from_attributes=True)
