from datetime import time

from sqlalchemy import ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models_base import Base
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, func
from datetime import  datetime

if TYPE_CHECKING:
    from app.models.classes import Class
    from app.models.teachers import Teacher


class Period(Base):
    __tablename__ = "periods"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    class_id: Mapped[int] = mapped_column(
        ForeignKey("classes.id"),
        nullable=False
    )

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id"),
        nullable=False
    )

    day: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    classroom: Mapped["Class"] = relationship(
        back_populates="periods"
    )

    teacher: Mapped["Teacher"] = relationship(
        back_populates="periods"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )