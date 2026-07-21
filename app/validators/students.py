from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.students import StudentNotFoundException
from app.models.students import Student


async def validate_student_exists(
    session: AsyncSession,
    student_id: int,
) -> Student:
    student = await session.get(Student, student_id)

    if student is None:
        raise StudentNotFoundException(student_id)

    return student