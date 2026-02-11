"""
Database connection and session management.
"""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings


# Create async engine
engine = create_async_engine(
    settings.async_database_url,
    echo=settings.api_debug,
    pool_pre_ping=True,
)

# Session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database sessions."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
