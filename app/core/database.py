from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Create async engine using the database URL from settings
engine = create_async_engine(settings.database_url, echo=False)

# Session factory for async database sessions
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    # Base class for all ORM models
    pass


async def get_db() -> AsyncSession:
    """Dependency that provides an async database session per request."""
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables() -> None:
    """Create all database tables on application startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)