from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.students import StudentCreate, StudentUpdate, StudentResponse
from app.services.student_service import StudentService

v1 = APIRouter()

@v1.post("/new-student", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(payload: StudentCreate, db: AsyncSession = Depends(get_db)):

    return await StudentService.create_student(db, payload)


@v1.get("/all-students", response_model=List[StudentResponse])
async def get_all_students(db: AsyncSession = Depends(get_db)):
    return await StudentService.get_all_students(db)

@v1.get("/fetch-one-student/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    return await StudentService.get_student(db, student_id)

@v1.put("/modify-student/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, payload: StudentUpdate, db: AsyncSession = Depends(get_db)):
    return await StudentService.update_student(db, student_id, payload)


@v1.delete("/delete-student/{student_id}")
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    await StudentService.delete_student(
        db,
        student_id,
    )
    return {
        "message": "Student record deleted successfully"
    }
