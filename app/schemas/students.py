from pydantic import  BaseModel, ConfigDict
from typing import  Optional

class StudentDetailsCreate(BaseModel):
    address_line_1: str
    address_line_2: Optional[str] = None
    state: str
    father_name: str

class StudentCreate(BaseModel):
    name: str
    phone_number: str
    roll_number: str
    grade: str
    details: StudentDetailsCreate

class StudentDetailsResponse(StudentDetailsCreate):
    model_config = ConfigDict(from_attributes=True)

class StudentResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    roll_number: str
    grade: str
    details: StudentDetailsResponse

    model_config = ConfigDict(from_attributes=True)

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    grade: Optional[str] = None