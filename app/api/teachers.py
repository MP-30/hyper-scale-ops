from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.teachers import TeacherCreate, TeacherResponse
from app.services.teacher_service import TeacherService

v1 = APIRouter()

@v1.post('/new-teacher', response_model=TeacherResponse, status_code=201)
async def create_teacher(payload: TeacherCreate, db: AsyncSession = Depends(get_db)):
    return await TeacherService.create_teacher(db, payload)

@v1.get('/all-teachers', response_model=list[TeacherResponse])
async def get_all_teachers(db: AsyncSession = Depends(get_db)):
    return await TeacherService.get_all_teachers(db)

@v1.get('/fetch-one-teacher/{teacher_id}', response_model=TeacherResponse)
async def fetch_one_teacher(teacher_id: int, db: AsyncSession = Depends(get_db)):
    teacher = await TeacherService.get_teacher(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher