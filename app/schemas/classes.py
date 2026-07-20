from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.students import StudentResponse
from app.schemas.periods import PeriodResponse

class ClassBase(BaseModel):
    name: str
    level: int

class ClassCreate(ClassBase):
    pass

class ClassUpdate(BaseModel):
    name: str | None = None
    level: int | None = None

class ClassResponse(ClassBase):
    id: int
    created_at: datetime
    updated_at: datetime
    students: list[StudentResponse] = []
    periods: list[PeriodResponse] = []

    model_config = ConfigDict(from_attributes=True)