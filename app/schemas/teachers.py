from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TeacherBase(BaseModel):
    name: str
    phone_number: str
    subject: str


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    name: str | None = None
    phone_number: str | None = None
    subject: str | None = None


class TeacherResponse(TeacherBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )