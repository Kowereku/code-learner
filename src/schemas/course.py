from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

from src.schemas.module import ModuleDetailRead


class CourseBase(BaseModel):
    name: str
    description: str | None = None
    icon_url: str | None = None


class CourseCreate(BaseModel):
    name: str
    description: str | None = None
    icon_url: str | None = None


class CourseListItem(BaseModel):
    id: int
    name: str
    description: str | None = None
    icon_url: str | None = None
    modules_count: int = 0

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def set_modules_count(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "modules_count" not in data and "modules" in data:
                modules = data.get("modules")
                data["modules_count"] = len(modules) if modules is not None else 0
            return data
        if hasattr(data, "modules"):
            modules = getattr(data, "modules", None)
            return {
                "id": getattr(data, "id", None),
                "name": getattr(data, "name", None),
                "description": getattr(data, "description", None),
                "icon_url": getattr(data, "icon_url", None),
                "modules_count": len(modules) if modules is not None else 0,
            }
        return data


class CourseDetail(BaseModel):
    id: int
    name: str
    description: str | None = None
    icon_url: str | None = None
    modules: list["ModuleDetailRead"] = []

    model_config = ConfigDict(from_attributes=True)
