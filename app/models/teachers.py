from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models_base import Base
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, func, String
from datetime import  datetime

if TYPE_CHECKING:
    from app.models.periods import Period

class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    subject: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    periods: Mapped[list["Period"]] = relationship(
        back_populates="teacher"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )