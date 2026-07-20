from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models_base import Base
from sqlalchemy import DateTime, func, String, ForeignKey
from datetime import  datetime

if TYPE_CHECKING:
    from app.models.classes import Class


class Student(Base):
    __tablename__ = "students"

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

    roll_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )

    class_id: Mapped[int] = mapped_column(
        ForeignKey("classes.id"),
        nullable=True
    )

    classroom: Mapped["Class"] = relationship(
        back_populates="students"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    details: Mapped["StudentDetails"] = relationship(
        back_populates="student",
        uselist=False,
        cascade="all, delete-orphan"
    )


class StudentDetails(Base):
    __tablename__ = "student_details"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey(
            "students.id",
            ondelete="CASCADE"
        ),
        unique=True,
        nullable=False
    )

    address_line_1: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    address_line_2: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    father_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    student: Mapped["Student"] = relationship(
        back_populates="details"
    )