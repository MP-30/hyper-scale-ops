import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Ensure pytest uses the test environment unless another ENV_FILE is already set.
os.environ.setdefault("ENV_FILE", ".env.test")

from app.main import app as fastapi_app
from app.core.database import (
    get_db,
    AsyncSessionLocal,
    engine
)

from app.core.models_base import Base
from app.models import all_models


# --- 1. SESSION SETUP (Runs ONCE for the whole test run) ---
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """Drops and rebuilds the database schema ONCE at the start of the test session.
    This guarantees your 'class_id' column is added without slowing down every test.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


# --- 2. FUNCTION SETUP (Runs before EVERY individual test) ---
@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_database() -> None:
    """Wipes data from the tables quickly between tests so they stay isolated."""
    async with AsyncSessionLocal() as session:
        # Combined into a single fast statement, including periods and classes
        await session.execute(
            text("TRUNCATE TABLE periods, teachers, classes, students, student_details RESTART IDENTITY CASCADE;")
        )
        await session.commit()
    yield


# --- 3. DATABASE SESSION FIXTURE ---
@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# --- 4. HTTPX ASYNC CLIENT FIXTURE ---
@pytest_asyncio.fixture(scope="function")
async def client():
    async def override_get_db():
        async with AsyncSessionLocal() as session:
            yield session

    fastapi_app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url="http://test",
    ) as ac:
        try:
            yield ac
        finally:
            fastapi_app.dependency_overrides.clear()