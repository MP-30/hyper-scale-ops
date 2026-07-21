from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.classes import (
    ClassCreate,
    ClassResponse,
    ClassUpdate,
)
from app.services.class_service import ClassService

v1 = APIRouter()


@v1.get(
    "/all-classes",
    response_model=list[ClassResponse],
)
async def get_all_classes(
    db: AsyncSession = Depends(get_db),
):
    return await ClassService.get_all_classes(db)


@v1.get(
    "/fetch-one-class/{class_id}",
    response_model=ClassResponse,
)
async def get_class(
    class_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await ClassService.get_class(
        db,
        class_id,
    )


@v1.post(
    "/new-class",
    response_model=ClassResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_class(
    payload: ClassCreate,
    db: AsyncSession = Depends(get_db),
):
    return await ClassService.create_class(
        db,
        payload,
    )


@v1.put(
    "/modify-class/{class_id}",
    response_model=ClassResponse,
)
async def update_class(
    class_id: int,
    payload: ClassUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await ClassService.update_class(
        db,
        class_id,
        payload,
    )


@v1.delete(
    "/delete-class/{class_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_class(
    class_id: int,
    db: AsyncSession = Depends(get_db),
):
    await ClassService.delete_class(
        db,
        class_id,
    )