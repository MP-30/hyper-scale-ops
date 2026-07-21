from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TeacherBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )
    phone_number: str
    subject: str = Field(
        min_length=2,
        max_length=100,
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value.replace(" ", "").isalpha():
            raise ValueError(
                "Name should contain only alphabetic characters."
            )

        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        value = value.strip()

        if not value.isdigit():
            raise ValueError(
                "Phone number must contain only digits."
            )

        if len(value) != 10:
            raise ValueError(
                "Phone number must be exactly 10 digits."
            )

        if value[0] not in "6789":
            raise ValueError(
                "Phone number must start with 6, 7, 8, or 9."
            )

        return value

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Subject name is too short."
            )

        return value.title()


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    phone_number: Optional[str] = None
    subject: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        value = value.strip()

        if not value.replace(" ", "").isalpha():
            raise ValueError(
                "Name should contain only alphabetic characters."
            )

        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        value = value.strip()

        if not value.isdigit():
            raise ValueError(
                "Phone number must contain only digits."
            )

        if len(value) != 10:
            raise ValueError(
                "Phone number must be exactly 10 digits."
            )

        if value[0] not in "6789":
            raise ValueError(
                "Phone number must start with 6, 7, 8, or 9."
            )

        return value

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Subject name is too short."
            )

        return value.title()


class TeacherResponse(TeacherBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )