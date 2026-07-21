from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.students import StudentResponse
from app.schemas.periods import PeriodResponse


class ClassBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
    )
    level: int = Field(
        ge=1,
        le=12,
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value.replace(" ", "").isalnum():
            raise ValueError(
                "Class name must contain only letters, numbers, and spaces."
            )

        return value


class ClassCreate(ClassBase):
    pass


class ClassUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
    )
    level: Optional[int] = Field(
        default=None,
        ge=1,
        le=12,
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        value = value.strip()

        if not value.replace(" ", "").isalnum():
            raise ValueError(
                "Class name must contain only letters, numbers, and spaces."
            )

        return value


class ClassResponse(ClassBase):
    id: int
    created_at: datetime
    updated_at: datetime

    students: list[StudentResponse] = Field(default_factory=list)
    periods: list[PeriodResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)