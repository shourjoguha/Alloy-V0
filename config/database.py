"""
Database Configuration for Alloy AI Fitness System.
Provides async engine, session factory, and FastAPI dependency.
"""

import os
import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

logger = logging.getLogger(__name__)


def _build_database_url() -> str:
    """Build the async PostgreSQL connection URL from environment variables."""
    host = os.getenv("DATABASE_HOST", "localhost")
    port = os.getenv("DATABASE_PORT", "5434")
    name = os.getenv("DATABASE_NAME", "Jacked-DB")
    user = os.getenv("DATABASE_USER", "jacked")
    password = os.getenv("DATABASE_PASSWORD", "jackedpass")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"


# Lazy-initialized globals — created on first use via `init_db()`.
_engine = None
_session_factory = None


def init_db() -> None:
    """Create the async engine and session factory.

    Call this once during application startup (e.g. in the FastAPI lifespan).
    """
    global _engine, _session_factory

    url = _build_database_url()
    _engine = create_async_engine(
        url,
        echo=os.getenv("DB_ECHO", "false").lower() == "true",
        pool_size=5,
        max_overflow=10,
    )
    _session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    logger.info("Database engine initialised (pool_size=5, max_overflow=10)")


async def close_db() -> None:
    """Dispose of the engine connection pool.

    Call this during application shutdown.
    """
    global _engine
    if _engine is not None:
        await _engine.dispose()
        logger.info("Database engine disposed")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async database session.

    Usage::

        @router.get("/example")
        async def example(db: AsyncSession = Depends(get_db)):
            ...
    """
    if _session_factory is None:
        raise RuntimeError(
            "Database not initialised. Call init_db() during application startup."
        )

    async with _session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
