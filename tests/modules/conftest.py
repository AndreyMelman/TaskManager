import logging
import uuid
import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from core.db import Base
from models import User, Note
from tests.test_config import engine, SessionFactory

log = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    log.info("Creating database tables for test...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def session():
    async with SessionFactory() as session:
        yield session

        await session.rollback()


@pytest.fixture(scope="function")
async def test_user(session: AsyncSession) -> User:
    user = User(email=f"test_user_{uuid.uuid4()}@example.com", hashed_password="pass")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def test_notes(test_user: User) -> list[Note]:
    notes = [
        Note(title="Title1", content="Note 1", user_id=test_user.id),
        Note(title="Title2", content="Note 2", user_id=test_user.id),
    ]
    return notes
