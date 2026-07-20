from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.teachers import Teacher
from app.schemas.teachers import TeacherCreate

class TeacherService:
    @staticmethod
    async def create_teacher(db: AsyncSession, payload: TeacherCreate):
        teacher = Teacher(**payload.model_dump())
        db.add(teacher)
        await db.commit()
        await db.refresh(teacher)
        return teacher

    @staticmethod
    async def get_all_teachers(db: AsyncSession):
        result = await db.execute(select(Teacher))
        return result.scalars().all()

    @staticmethod
    async def get_teacher(db: AsyncSession, teacher_id: int):
        result = await db.execute(
            select(Teacher)
            .options(selectinload(Teacher.periods))
            .where(Teacher.id == teacher_id)
        )
        return result.scalar_one_or_none()