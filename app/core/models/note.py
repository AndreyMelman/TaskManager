from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import TimestampMixin


class Note(Base, TimestampMixin):

    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str]




