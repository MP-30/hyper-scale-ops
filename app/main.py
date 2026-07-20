from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
from fastapi.staticfiles import StaticFiles

# Core Database & Models
from app.core.database import get_db
import app.models.all_models

# Routers
from app.api.pages import pages_router
from app.api.students import v1 as students_router
from app.api.classes import v1 as class_router
from app.api.teachers import v1 as teacher_router
from app.api.periods import v1 as periods_router  # Added missing import

BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(
    title="Hyper-Scale-Ops-API",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR/"static"),
    name="static",
)

# Static Pages Router
app.include_router(pages_router)

# Core API Routers - Unified under /api/v1
app.include_router(students_router, prefix="/api/v1", tags=["Students"])
app.include_router(class_router, prefix="/api/v1", tags=["Classes"])
app.include_router(teacher_router, prefix="/api/v1/teachers", tags=["Teachers"])
app.include_router(periods_router, prefix="/api/v1/periods", tags=["Periods"]) # Added missing registration

@app.get("/healthcheck/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/db-check")
async def check_database(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )

@app.get("/debug-tables")
async def debug_tables(db: AsyncSession = Depends(get_db)):
    query = text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    result = await db.execute(query)
    tables = [row[0] for row in result.fetchall()]
    return {"tables_found_by_fastapi": tables}