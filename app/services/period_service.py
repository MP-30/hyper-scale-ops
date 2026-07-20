from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.periods import Period
from app.schemas.periods import PeriodCreate

class PeriodService:
    @staticmethod
    async def create_period(db: AsyncSession, payload: PeriodCreate):
        period = Period(**payload.model_dump())
        db.add(period)
        await db.commit()
        await db.refresh(period, ["teacher", "classroom"])
        return period

    @classmethod
    async def get_all_periods(cls, db: AsyncSession):
        result = await db.execute(
            select(Period).options(
                selectinload(Period.classroom),
                selectinload(Period.teacher),
            )
        )
        return result.scalars().all()

    @staticmethod
    async def get_period(db: AsyncSession, period_id: int):
        result = await db.execute(
            select(Period)
            .options(selectinload(Period.teacher), selectinload(Period.classroom))
            .where(Period.id == period_id)
        )
        return result.scalar_one_or_none()