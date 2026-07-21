from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.logger import app_logger
from app.exceptions.classes import ClassNotFoundException
from app.models.classes import Class
from app.models.students import Student
from app.models.periods import Period
from app.schemas.classes import (
    ClassCreate,
    ClassUpdate,
)


class ClassService:
    @staticmethod
    async def get_all_classes(
        db: AsyncSession,
    ):
        app_logger.info("Fetching all classes")
        result = await db.execute(
            select(Class).options(
                selectinload(Class.students).selectinload(Student.details),
                selectinload(Class.periods).selectinload(Period.teacher),
            )
        )
        return result.scalars().all()

    @staticmethod
    async def get_class(
        db: AsyncSession,
        class_id: int,
    ):
        app_logger.info(f"Fetching class {class_id}")
        result = await db.execute(
            select(Class)
            .options(
                selectinload(Class.students).selectinload(Student.details),
                selectinload(Class.periods).selectinload(Period.teacher),
            )
            .where(Class.id == class_id)
        )
        classroom = result.scalar_one_or_none()
        if classroom is None:
            raise ClassNotFoundException(class_id)
        return classroom

    @staticmethod
    async def create_class(
        db: AsyncSession,
        payload: ClassCreate,
    ):
        app_logger.info(f"Creating class '{payload.name}'")
        try:
            classroom = Class(
                name=payload.name,
                level=payload.level,
            )
            db.add(classroom)
            await db.commit()
            await db.refresh(
                classroom,
                attribute_names=[
                    "students",
                    "periods",
                ],
            )
            app_logger.info(f"Class created successfully. id={classroom.id}")
            return classroom
        except Exception:
            await db.rollback()
            app_logger.exception("Failed creating class")
            raise

    @staticmethod
    async def update_class(
        db: AsyncSession,
        class_id: int,
        payload: ClassUpdate,
    ):
        app_logger.info(f"Updating class {class_id}")
        classroom = await ClassService.get_class(
            db,
            class_id,
        )
        try:
            data = payload.model_dump(
                exclude_unset=True,
            )
            for key, value in data.items():
                setattr(
                    classroom,
                    key,
                    value,
                )
            await db.commit()
            app_logger.info(f"Class updated successfully. id={class_id}")
            return await ClassService.get_class(
                db,
                class_id,
            )
        except Exception:
            await db.rollback()
            app_logger.exception(f"Failed updating class {class_id}")
            raise

    @staticmethod
    async def delete_class(
        db: AsyncSession,
        class_id: int,
    ):
        app_logger.info(f"Deleting class {class_id}")
        classroom = await ClassService.get_class(
            db,
            class_id,
        )
        try:
            await db.delete(classroom)
            await db.commit()
            app_logger.info(f"Class deleted successfully. id={class_id}")
        except Exception:
            await db.rollback()
            app_logger.exception(f"Failed deleting class {class_id}")
            raise
