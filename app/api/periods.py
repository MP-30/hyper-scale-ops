from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.periods import PeriodCreate, PeriodResponse
from app.services.period_service import PeriodService

v1 = APIRouter()

@v1.post('/new-period', response_model=PeriodResponse, status_code=201)
async def create_period(payload: PeriodCreate, db: AsyncSession = Depends(get_db)):
    return await PeriodService.create_period(db, payload)

@v1.get('/all-periods', response_model=list[PeriodResponse])
async def get_all_periods(db: AsyncSession = Depends(get_db)):
    return await PeriodService.get_all_periods(db)

@v1.get('/fetch-one-period/{period_id}', response_model=PeriodResponse)
async def fetch_one_period(period_id: int, db: AsyncSession = Depends(get_db)):
    period = await PeriodService.get_period(db, period_id)
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    return period