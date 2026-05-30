from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.students import StudentCreate, StudentResponse, StudentUpdate
from app.services.student import StudentService

v1 = APIRouter()

@v1.get('/all-students', response_model=list[StudentResponse])
async def get_student(
        db: AsyncSession = Depends(get_db)
):
    return  await StudentService.get_all_students(db)

@v1.get('/fetch-one-student/{student_id}', response_model=StudentResponse)
async def fetch_one(
        student_id: int,
        db: AsyncSession = Depends(get_db)
):
    student = await StudentService.get_student(
        db, student_id
    )
    if not student:
        raise HTTPException(
            status_code= 404,
            detail="Student not found"
        )
    return student
@v1.post('/new-student' , response_model=StudentResponse, status_code=201)
async def add_one_student(
        payload: StudentCreate,
        db: AsyncSession = Depends(get_db)
):
    return  await StudentService.create_student(db,payload)


@v1.put('/modify-student/{student_id}', response_model=StudentResponse)
async def modify_student(
        student_id:int,
        payload: StudentUpdate,
        db: AsyncSession = Depends(get_db)
):
    student = await StudentService.update_student(
        db, student_id, payload
    )

    if not student:
        raise HTTPException(
            status_code= 404,
            detail="Student not found"
        )
    return  student

@v1.delete('/delete-student/{student_id}')
async def delete_student(
        student_id: int,
        db: AsyncSession= Depends(get_db)
):
    deleted = await StudentService.delete_student(
        db, student_id
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "message": "Student deleted successfully"
    }