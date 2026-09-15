import enum

from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.db import Base


class ExerciseType(str, enum.Enum):
    multiple_choice = "multiple_choice"
    code = "code"
    fill_in_blank = "fill_in_blank"
    true_false = "true_false"
    block_assembly = "block_assembly"
    matching = "matching"


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    lesson_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    code_snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)

    lesson: Mapped["Lesson"] = relationship(back_populates="exercises")
