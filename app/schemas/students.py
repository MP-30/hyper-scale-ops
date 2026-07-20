from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# --- STUDENT DETAILS SCHEMAS ---
class StudentDetailBase(BaseModel):
    address_line_1: str
    address_line_2: Optional[str] = None
    state: str
    father_name: str

class StudentDetailCreate(StudentDetailBase):
    pass

class StudentDetailResponse(StudentDetailBase):
    id: int
    student_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- CORE STUDENT SCHEMAS ---
class StudentBase(BaseModel):
    name: str
    phone_number: str
    roll_number: str
    class_id: Optional[int] = None

class StudentCreate(StudentBase):
    details: StudentDetailCreate  # Nested details required on signup

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    roll_number: Optional[str] = None
    class_id: Optional[int] = None
    details: Optional[StudentDetailCreate] = None

class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    details: Optional[StudentDetailResponse] = None # Automatically populates

    model_config = ConfigDict(from_attributes=True)