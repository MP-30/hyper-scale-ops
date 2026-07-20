from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models_base import Base
from sqlalchemy import DateTime, func, String
from datetime import  datetime

if TYPE_CHECKING:
    from app.models.students import Student
    from app.models.periods import Period

class Class(Base):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    level: Mapped[int] = mapped_column(
        nullable=False
    )

    students: Mapped[list["Student"]] = relationship(
        back_populates="classroom"
    )

    periods: Mapped[list["Period"]] = relationship(
        back_populates="classroom"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )