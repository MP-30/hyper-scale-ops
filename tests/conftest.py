import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from testcontainers.postgres import PostgresContainer

from app.main import app
from app.core.database import get_db
from app.core.models_base import Base


# ------------------------------------------------------------------
# Global session factory
# ------------------------------------------------------------------

TestingSessionLocal: async_sessionmaker[AsyncSession] | None = None


# ------------------------------------------------------------------
# Tell pytest to use asyncio
# ------------------------------------------------------------------

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# ------------------------------------------------------------------
# Create PostgreSQL TestContainer once
# ------------------------------------------------------------------

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    global TestingSessionLocal

    with PostgresContainer("postgres:16-alpine") as postgres:

        sync_url = postgres.get_connection_url()

        async_url = sync_url.replace(
            "postgresql+psycopg2://",
            "postgresql+asyncpg://",
        )

        engine = create_async_engine(
            async_url,
            echo=False,
        )

        TestingSessionLocal = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield

        # Drop tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await engine.dispose()


# ------------------------------------------------------------------
# One DB session per test
# ------------------------------------------------------------------

@pytest_asyncio.fixture
async def db_session():

    assert TestingSessionLocal is not None

    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()