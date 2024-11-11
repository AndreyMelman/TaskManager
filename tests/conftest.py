import logging
import uuid

from core.db import Base
from tests.test_config import engine, SessionFactory
import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Note
from tests.utils.user import create_super_user

from tests.utils.utils import get_superuser_token_headers, truncate_table

log = logging.getLogger(__name__)

pytest_plugins = "pytest_asyncio"


@pytest.fixture(scope="session", autouse=True)
def set_logging_level():
    logging.getLogger().setLevel(logging.WARNING)


@pytest.fixture(scope="function", autouse=True)
async def setup_db():
    log.info("Creating database tables for test...")
    async with engine.begin() as conn:
        await truncate_table(conn)


@pytest.fixture(scope="function")
async def session():
    async with SessionFactory() as session:
        yield session

        await session.rollback()


@pytest.fixture(scope="function")
async def superuser(session: AsyncSession):
    return await create_super_user(session=session)


@pytest.fixture(scope="function")
async def superuser_token_headers():
    return await get_superuser_token_headers()
