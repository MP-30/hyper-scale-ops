from fastapi import FastAPI, Depends, HTTPException
from app.api.students import v1 as students_router
from sqlalchemy.sql import text
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(
    title="Hyper-Scale-Ops-API",)


app.include_router(students_router, prefix="/api", tags=["Students"])


@app.get("/healthcheck/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/db-check")
async def check_database(db: AsyncSession = Depends(get_db)):
    try:
        # Executes standard connectivity verification non-blockingly
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )

@app.get("/debug-tables")
async def debug_tables(db: AsyncSession = Depends(get_db)):
    # Query PostgreSQL's system catalog for tables in the public schema
    query = text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    result = await db.execute(query)
    tables = [row[0] for row in result.fetchall()]
    return {"tables_found_by_fastapi": tables}
