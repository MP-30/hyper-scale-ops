from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.teachers import Teacher
from app.schemas.teachers import TeacherCreate, TeacherUpdate
from app.exceptions.teachers import TeacherNotFoundException
from app.core.logger import app_logger

class TeacherService:
    @staticmethod
    async def create_teacher(
        db: AsyncSession,
        payload: TeacherCreate,
    ):
        app_logger.info(f"Creating teacher '{payload.name}'")
        try:
            teacher = Teacher(**payload.model_dump())
            db.add(teacher)
            await db.commit()
            await db.refresh(teacher)
            app_logger.info(f"Teacher created successfully. id={teacher.id}")
            return teacher
        except Exception:
            await db.rollback()
            app_logger.exception("Failed to create teacher")
            raise

    @staticmethod
    async def get_all_teachers(
        db: AsyncSession,
    ):
        app_logger.info("Fetching all teachers")
        result = await db.execute(select(Teacher))
        return result.scalars().all()

    @staticmethod
    async def get_teacher(
        db: AsyncSession,
        teacher_id: int,
    ):
        app_logger.info(f"Fetching teacher {teacher_id}")
        result = await db.execute(
            select(Teacher)
            .options(selectinload(Teacher.periods))
            .where(Teacher.id == teacher_id)
        )
        teacher = result.scalar_one_or_none()
        if teacher is None:
            raise TeacherNotFoundException(teacher_id)
        return teacher

    @staticmethod
    async def update_teacher(
        db: AsyncSession,
        teacher_id: int,
        payload: TeacherUpdate,
    ):
        app_logger.info(f"Updating teacher {teacher_id}")
        teacher = await TeacherService.get_teacher(
            db,
            teacher_id,
        )
        try:
            data = payload.model_dump(
                exclude_unset=True,
            )
            for key, value in data.items():
                setattr(
                    teacher,
                    key,
                    value,
                )
            await db.commit()
            await db.refresh(teacher)
            app_logger.info(f"Teacher updated successfully. id={teacher_id}")
            return teacher
        except Exception:
            await db.rollback()
            app_logger.exception(f"Failed updating teacher {teacher_id}")
            raise

    @staticmethod
    async def delete_teacher(
        db: AsyncSession,
        teacher_id: int,
    ):
        app_logger.info(f"Deleting teacher {teacher_id}")
        teacher = await TeacherService.get_teacher(
            db,
            teacher_id,
        )
        try:
            await db.delete(teacher)
            await db.commit()
            app_logger.info(f"Teacher deleted successfully. id={teacher_id}")
        except Exception:
            await db.rollback()
            app_logger.exception(f"Failed deleting teacher {teacher_id}")
            raise