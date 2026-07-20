from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.classes import Class
from app.models.students import Student
from app.models.periods import Period
from app.schemas.classes import (
    ClassCreate,
    ClassUpdate,
)


class ClassService:
    @staticmethod
    async def get_all_classes(db: AsyncSession):
        result = await db.execute(
            select(Class).options(
                selectinload(Class.students).selectinload(Student.details),
                selectinload(Class.periods).selectinload(Period.teacher),
            )
        )
        return result.scalars().all()

    @staticmethod
    async def get_class(db: AsyncSession, class_id: int):
        result = await db.execute(
            select(Class)
            .options(
                selectinload(Class.students).selectinload(Student.details),
                selectinload(Class.periods).selectinload(Period.teacher),
            )
            .where(Class.id == class_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_class(db: AsyncSession, payload: ClassCreate):
        classroom = Class(
            name=payload.name,
            level=payload.level,
        )

        db.add(classroom)
        await db.commit()

        # FIX HERE: Explicitly pass the relationship fields to attribute_names
        await db.refresh(classroom, attribute_names=["students", "periods"])

        return classroom

    @staticmethod
    async def update_class(db: AsyncSession, class_id: int, payload: ClassUpdate):
        classroom = await ClassService.get_class(db, class_id)

        if not classroom:
            return None

        update_data = payload.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(classroom, key, value)

        await db.commit()

        # FIX HERE TOO: Re-fetch using our clean get_class method so relationships are correctly loaded
        return await ClassService.get_class(db, class_id)

    @staticmethod
    async def delete_class(db: AsyncSession, class_id: int):
        classroom = await ClassService.get_class(db, class_id)

        if not classroom:
            return False

        await db.delete(classroom)
        await db.commit()

        return True
