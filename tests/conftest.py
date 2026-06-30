import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import  AsyncSession
from app.main import app
from sqlalchemy import text
from app.core.database import (
    get_db,
    AsyncSessionLocal
)

# telling anyIO to use asyncio
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

# database session.. one fresh SQLAlchemy session per test

@pytest_asyncio.fixture()
async def db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# fastapi test client and override get_db() dependency

@pytest_asyncio.fixture
async def client(db_session: AsyncSession):

    async def override_get_db():
        yield db_session

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
async def clean_database():
    async with AsyncSessionLocal() as session:
        # Child table first
        await session.execute(text("TRUNCATE TABLE student_details RESTART IDENTITY CASCADE;"))

        # Parent table
        await session.execute(text("TRUNCATE TABLE students RESTART IDENTITY CASCADE;"))

        await session.commit()