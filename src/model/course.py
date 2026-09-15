from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, synonym

from src.model.db import Base

if TYPE_CHECKING:
    from src.model.module import Module
    from src.model.user_course import UserCourse


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    title = synonym("name")

    modules: Mapped[list[Module]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Module.order_index",
    )
    user_links: Mapped[list[UserCourse]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
