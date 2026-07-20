from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.students import StudentCreate, StudentUpdate, StudentResponse
from app.services.student_service import StudentService

v1 = APIRouter()

@v1.post("/new-student", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(payload: StudentCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await StudentService.create_student(db, payload)
    except Exception as e:
        # Catches foreign key issues like setting a class_id that doesn't exist
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create student. Ensure class_id is valid. Error: {str(e)}"
        )

@v1.get("/all-students", response_model=List[StudentResponse])
async def get_all_students(db: AsyncSession = Depends(get_db)):
    return await StudentService.get_all_students(db)

@v1.get("/fetch-one-student/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await StudentService.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student record not found")
    return student

@v1.put("/modify-student/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, payload: StudentUpdate, db: AsyncSession = Depends(get_db)):
    student = await StudentService.update_student(db, student_id, payload)
    if not student:
        raise HTTPException(status_code=404, detail="Student record not found")
    return student

@v1.delete("/delete-student/{student_id}")
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    success = await StudentService.delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student record not found")
    return {"message": "Student record deleted successfully"}