from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.periods import Period
from app.schemas.periods import PeriodCreate
from app.core.logger import app_logger
from app.exceptions.periods import PeriodNotFoundException
from app.schemas.periods import (
    PeriodCreate,
    PeriodUpdate,
)

class PeriodService:
    @staticmethod
    async def create_period(
        db: AsyncSession,
        payload: PeriodCreate,
    ):
        app_logger.info(f"Creating period '{payload.name}'")
        try:
            period = Period(**payload.model_dump())
            db.add(period)
            await db.commit()
            await db.refresh(
                period,
                attribute_names=[
                    "teacher",
                    "classroom",
                ],
            )
            app_logger.info(f"Period created successfully. id={period.id}")
            return period
        except Exception:
            await db.rollback()
            app_logger.exception("Failed creating period")
            raise

    @staticmethod
    async def get_all_periods(
        db: AsyncSession,
    ):
        app_logger.info("Fetching all periods")
        result = await db.execute(
            select(Period).options(
                selectinload(Period.classroom),
                selectinload(Period.teacher),
            )
        )
        return result.scalars().all()

    @staticmethod
    async def get_period(
        db: AsyncSession,
        period_id: int,
    ):
        app_logger.info(f"Fetching period {period_id}")
        result = await db.execute(
            select(Period)
            .options(
                selectinload(Period.teacher),
                selectinload(Period.classroom),
            )
            .where(Period.id == period_id)
        )
        period = result.scalar_one_or_none()
        if period is None:
            raise PeriodNotFoundException(period_id)
        return period

    @staticmethod
    async def update_period(
        db: AsyncSession,
        period_id: int,
        payload: PeriodUpdate,
    ):
        app_logger.info(f"Updating period {period_id}")
        period = await PeriodService.get_period(
            db,
            period_id,
        )
        try:
            data = payload.model_dump(
                exclude_unset=True,
            )
            for key, value in data.items():
                setattr(
                    period,
                    key,
                    value,
                )
            await db.commit()
            await db.refresh(
                period,
                attribute_names=[
                    "teacher",
                    "classroom",
                ],
            )
            app_logger.info(f"Period updated successfully. id={period_id}")
            return period
        except Exception:
            await db.rollback()
            app_logger.exception(f"Failed updating period {period_id}")
            raise

    @staticmethod
    async def delete_period(
        db: AsyncSession,
        period_id: int,
    ):
        app_logger.info(f"Deleting period {period_id}")
        period = await PeriodService.get_period(
            db,
            period_id,
        )
        try:
            await db.delete(period)
            await db.commit()
            app_logger.info(f"Period deleted successfully. id={period_id}")
        except Exception:
            await db.rollback()
            app_logger.exception(f"Failed deleting period {period_id}")
            raise