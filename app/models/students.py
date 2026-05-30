from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.models_base import Base


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

    grade: Mapped[str] = mapped_column(
        String(20),
        nullable=False
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

    student: Mapped["Student"] = relationship(
        back_populates="details"
    )