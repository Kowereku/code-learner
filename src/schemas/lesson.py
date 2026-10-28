from pydantic import BaseModel, ConfigDict, Field

from src.schemas.exercise import ExerciseRead
from src.schemas.localized import Localized


class LessonBase(BaseModel):
    title: str
    xp_reward: int = 0


class LessonCreate(BaseModel):
    title: str
    xp_reward: int = 0


class LessonRead(Localized):
    id: int
    module_id: int
    title: str
    xp_reward: int = 0
    is_quiz: bool = False

    model_config = ConfigDict(from_attributes=True)


class LessonDetailRead(Localized):
    id: int
    module_id: int
    title: str
    xp_reward: int = 0
    is_quiz: bool = False
    exercises: list[ExerciseRead] = []

    model_config = ConfigDict(from_attributes=True)


class LessonComplete(BaseModel):
    mistakes_made: int = Field(default=0, ge=0)
    # Code exercises of this lesson solved by typing in this run; each counts once per user, ever.
    code_exercise_ids: list[int] = Field(default_factory=list, max_length=100)
