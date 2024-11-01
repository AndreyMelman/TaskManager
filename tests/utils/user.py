from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from tests.utils.utils import random_email, random_lower_string

from fastapi_users.password import PasswordHelper
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher


async def create_random_user(session: AsyncSession) -> User:
    email = await random_email()
    password = await random_lower_string()
    user = User(email=email, hashed_password=password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def create_super_user(session: AsyncSession) -> User:
    password_hash = PasswordHash((Argon2Hasher(),))
    password_helper = PasswordHelper(password_hash)
    email = await random_email()
    password = await random_lower_string()
    user = User(email="1@1.com", hashed_password=password_helper.hash("1"))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
