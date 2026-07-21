from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.periods import PeriodNotFoundException
from app.models.periods import Period


async def validate_period_exists(
    session: AsyncSession,
    period_id: int,
) -> Period:
    period = await session.get(Period, period_id)

    if period is None:
        raise PeriodNotFoundException(period_id)

    return period