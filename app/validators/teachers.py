from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.teachers import TeacherNotFoundException
from app.models.teachers import Teacher


async def validate_teacher_exists(
    session: AsyncSession,
    teacher_id: int,
) -> Teacher:
    teacher = await session.get(Teacher, teacher_id)

    if teacher is None:
        raise TeacherNotFoundException(teacher_id)

    return teacher