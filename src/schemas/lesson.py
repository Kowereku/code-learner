from pydantic import BaseModel, ConfigDict

from src.schemas.exercise import ExerciseRead


class LessonBase(BaseModel):
    title: str
    xp_reward: int = 0


class LessonCreate(BaseModel):
    title: str
    xp_reward: int = 0


class LessonRead(BaseModel):
    id: int
    module_id: int
    title: str
    xp_reward: int = 0

    model_config = ConfigDict(from_attributes=True)


class LessonDetailRead(BaseModel):
    id: int
    module_id: int
    title: str
    xp_reward: int = 0
    exercises: list[ExerciseRead] = []

    model_config = ConfigDict(from_attributes=True)
