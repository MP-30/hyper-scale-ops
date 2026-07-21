from datetime import datetime, time
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.teachers import TeacherResponse


class WeekDay(str, Enum):
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"
    saturday = "Saturday"


class PeriodBase(BaseModel):
    class_id: int = Field(gt=0)
    teacher_id: int = Field(gt=0)
    day: WeekDay
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.start_time >= self.end_time:
            raise ValueError("End time must be later than start time.")

        if self.start_time < time(7, 0):
            raise ValueError("School cannot start before 07:00.")

        if self.end_time > time(18, 0):
            raise ValueError("School cannot end after 18:00.")

        return self


class PeriodCreate(PeriodBase):
    pass


class PeriodUpdate(BaseModel):
    class_id: Optional[int] = Field(default=None, gt=0)
    teacher_id: Optional[int] = Field(default=None, gt=0)
    day: Optional[WeekDay] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

    @model_validator(mode="after")
    def validate_time_range(self):
        if (
            self.start_time is not None
            and self.end_time is not None
            and self.start_time >= self.end_time
        ):
            raise ValueError("End time must be later than start time.")

        return self


class PeriodResponse(PeriodBase):
    id: int
    created_at: datetime
    updated_at: datetime
    teacher: TeacherResponse | None = None

    model_config = ConfigDict(from_attributes=True)