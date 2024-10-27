from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
)

from core.config import settings



DATABASE_URL = str(settings.db.url)

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

SessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


