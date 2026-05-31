from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.db import Base

if TYPE_CHECKING:
    from src.model.lesson import Lesson
    from src.model.user import User


class UserLesson(Base):
    __tablename__ = "user_lessons"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    lesson_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("lessons.id", ondelete="CASCADE"),
        primary_key=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    mistakes_made: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0, server_default="0"
    )

    user: Mapped[User] = relationship(back_populates="lesson_links")
    lesson: Mapped[Lesson] = relationship(back_populates="user_links")
