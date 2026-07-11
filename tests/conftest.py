import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Ensure pytest uses the test environment unless another ENV_FILE is already set.
os.environ.setdefault("ENV_FILE", ".env.test")

from app.main import app
from app.core.database import (
    get_db,
    AsyncSessionLocal
)

# fastapi test client and override get_db() dependency

@pytest_asyncio.fixture()
async def db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@pytest_asyncio.fixture
async def client():

    async def override_get_db():
        async with AsyncSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        try:
            yield client
        finally:
            app.dependency_overrides.clear()

@pytest_asyncio.fixture(autouse=True)
async def clean_database() -> None:
    async with AsyncSessionLocal() as session:
        await session.execute(text("TRUNCATE TABLE student_details RESTART IDENTITY CASCADE;"))
        await session.execute(text("TRUNCATE TABLE students RESTART IDENTITY CASCADE;"))
        await session.commit()