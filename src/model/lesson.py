from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.db import Base

if TYPE_CHECKING:
    from src.model.exercise import Exercise
    from src.model.module import Module
    from src.model.user_lesson import UserLesson


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    module_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    xp_reward: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0, server_default="0"
    )

    module: Mapped[Module] = relationship(back_populates="lessons")
    exercises: Mapped[list[Exercise]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan"
    )
    user_links: Mapped[list[UserLesson]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan"
    )
