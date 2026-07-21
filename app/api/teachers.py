from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.teachers import TeacherCreate, TeacherResponse
from app.services.teacher_service import TeacherService
from typing import List
v1 = APIRouter()


@v1.post(
    "/new-teacher",
    response_model=TeacherResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_teacher(
    payload: TeacherCreate,
    db: AsyncSession = Depends(get_db),
):
    return await TeacherService.create_teacher(
        db,
        payload,
    )


@v1.get(
    "/all-teachers",
    response_model=List[TeacherResponse],
)
async def get_all_teachers(
    db: AsyncSession = Depends(get_db),
):
    return await TeacherService.get_all_teachers(db)


@v1.get(
    "/fetch-one-teacher/{teacher_id}",
    response_model=TeacherResponse,
)
async def get_teacher(
    teacher_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await TeacherService.get_teacher(
        db,
        teacher_id,
    )