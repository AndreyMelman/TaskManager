import asyncio
import logging

import pytest

from core.db import Base
from tests.test_config import engine, SessionFactory


pytest_plugins = "pytest_asyncio"
log = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
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
