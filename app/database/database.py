"""
Database connection and session management
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool

from app.config import settings
from .models import Base


# Create async engine
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    poolclass=NullPool,  # Use NullPool for better async support
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def init_db() -> None:
    """
    Initialize database tables
    
    Note: In production, use Alembic migrations instead
    """
    async with engine.begin() as conn:
        # Drop all tables (only for development!)
        # await conn.run_sync(Base.metadata.drop_all)
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting database session
    
    Usage in handlers:
        async with get_db() as session:
            # Use session here
            pass
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def close_db() -> None:
    """Close database connections"""
    await engine.dispose()
