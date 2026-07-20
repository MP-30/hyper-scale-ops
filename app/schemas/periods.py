from datetime import datetime, time
from app.schemas.teachers import TeacherResponse
from pydantic import BaseModel, ConfigDict


class PeriodBase(BaseModel):
    class_id: int
    teacher_id: int
    day: str
    start_time: time
    end_time: time


class PeriodCreate(PeriodBase):
    pass


class PeriodUpdate(BaseModel):
    class_id: int | None = None
    teacher_id: int | None = None
    day: str | None = None
    start_time: time | None = None
    end_time: time | None = None


class PeriodResponse(PeriodBase):
    id: int
    created_at: datetime
    updated_at: datetime
    teacher: TeacherResponse | None = None # Includes teacher details when fetched

    model_config = ConfigDict(from_attributes=True)