from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from core.db import db_helper
from models import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.getter_session),
    ]
):
    yield User.get_db(session=session)
