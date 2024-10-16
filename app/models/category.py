from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from .mixins.int_id_pk import IntIdPkMixin
from .mixins.user_relation import UserRelationMixin


class Category(UserRelationMixin, IntIdPkMixin, Base):
    __tablename__ = "categories"

    _user_back_populates = "categories"

    name: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True,
    )

    tasks = relationship("Task", back_populates="category")
