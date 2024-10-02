from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from .mixins.int_id_pk import IntIdPkMixin


if TYPE_CHECKING:
    from .task import Task
    from .note import Note


class User(IntIdPkMixin, Base):

    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), unique=True)
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
