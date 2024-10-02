from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base
from .mixins.int_id_pk import IntIdPkMixin
from .mixins.user_relation import UserRelationMixin


class Note(UserRelationMixin, IntIdPkMixin, Base):
    _user_back_populates = "notes"

    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(String(50000), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=datetime.now(),
    )
