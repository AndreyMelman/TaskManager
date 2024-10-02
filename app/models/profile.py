from datetime import date

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base
from models.mixins.int_id_pk import IntIdPkMixin
from models.mixins.user_relation import UserRelationMixin


class Profile(UserRelationMixin, IntIdPkMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profiles"

    first_name: Mapped[str | None] = mapped_column(String(32))
    last_name: Mapped[str | None] = mapped_column(String(32))
    bio: Mapped[str | None] = mapped_column(String(5000))
    phone_number: Mapped[str | None] = mapped_column(String(32))
    address: Mapped[str | None] = mapped_column(String(64))
    date_of_birth: Mapped[date | None]
