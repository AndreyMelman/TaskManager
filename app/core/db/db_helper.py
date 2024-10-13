import logging
from typing import AsyncGenerator

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from core.config import settings

log = logging.getLogger(__name__)


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        max_overflow: int = 10,
        pool_size: int = 5,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        try:
            await self.engine.dispose()
        except SQLAlchemyError as e:
            log.error("Database error: %r", e)
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
            )

    async def getter_session(self) -> AsyncGenerator[AsyncSession, None]:
        try:
            async with self.session_factory() as session:
                log.info("Starting database session and transaction")
                yield session
                log.info("Session created and transaction committed successfully")
            log.info("Session closed successfully")
        except SQLAlchemyError as e:
            log.error(
                "Database error during transaction: %r. Rolling back transaction.", e
            )
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
            )
        except Exception as e:
            log.error("Unexpected error: %r. Transaction might not be committed.", e)
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error"
            )


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    max_overflow=settings.db.max_overflow,
    pool_size=settings.db.pool_size,
)
