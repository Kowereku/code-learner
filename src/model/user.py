from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.db import Base

if TYPE_CHECKING:
    from src.model.user_course import UserCourse
    from src.model.user_lesson import UserLesson


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    total_xp: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0, server_default="0"
    )
    streak_days: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0, server_default="0"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    course_links: Mapped[list[UserCourse]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    lesson_links: Mapped[list[UserLesson]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
