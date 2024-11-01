import logging
import uuid
import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from core.db import Base
from models import User, Note
from tests.test_config import engine, SessionFactory

log = logging.getLogger(__name__)

from fastapi_users.password import PasswordHelper
from pwdlib import PasswordHash, exceptions
from pwdlib.hashers.argon2 import Argon2Hasher



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
    password_hash = PasswordHash((
        Argon2Hasher(),
    ))
    password_helper = PasswordHelper(password_hash)

    user = User(email="1@1.com", hashed_password=password_helper.hash('1'))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
