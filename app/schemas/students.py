from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudentDetailBase(BaseModel):
    address_line_1: str = Field(min_length=5, max_length=200)
    address_line_2: Optional[str] = Field(default=None, max_length=200)
    state: str = Field(min_length=2, max_length=100)
    father_name: str = Field(min_length=2, max_length=100)

    @field_validator("address_line_1", "state", "father_name")
    @classmethod
    def strip_strings(cls, value: str) -> str:
        return value.strip()


class StudentDetailCreate(StudentDetailBase):
    pass


class StudentDetailResponse(StudentDetailBase):
    id: int
    student_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class StudentBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone_number: str
    roll_number: str = Field(min_length=2, max_length=30)
    class_id: Optional[int] = Field(default=None, gt=0)

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

    @field_validator("roll_number")
    @classmethod
    def validate_roll_number(cls, value: str) -> str:
        value = value.strip().upper()

        if len(value) < 2:
            raise ValueError(
                "Roll number is too short."
            )

        return value


class StudentCreate(StudentBase):
    details: StudentDetailCreate


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    phone_number: Optional[str] = None
    roll_number: Optional[str] = Field(default=None, min_length=2, max_length=30)
    class_id: Optional[int] = Field(default=None, gt=0)
    details: Optional[StudentDetailCreate] = None

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

    @field_validator("roll_number")
    @classmethod
    def validate_roll_number(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        return value.strip().upper()


class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    details: Optional[StudentDetailResponse] = None

    model_config = ConfigDict(from_attributes=True)