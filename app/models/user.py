from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from core.types.user_id import UserIdType
from .mixins.int_id_pk import IntIdPkMixin

from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase


if TYPE_CHECKING:
    from .task import Task
    from .note import Note
    # from .profile import Profile
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=datetime.now(),
    )

    tasks: Mapped[list["Task"]] = relationship(back_populates="user")
    notes: Mapped[list["Note"]] = relationship(back_populates="user")
    # profiles: Mapped[list["Profile"]] = relationship(back_populates="user")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
