from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.classes import ClassNotFoundException
from app.models.classes import Class


async def validate_class_exists(
    session: AsyncSession,
    class_id: int,
) -> Class:
    obj = await session.get(Class, class_id)

    if obj is None:
        raise ClassNotFoundException(class_id)

    return obj