from datetime import datetime, UTC

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from .mixins import TimestampMixin


class Task(Base, TimestampMixin):

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(15))
    deadline_at: Mapped[datetime]
    completed: Mapped[bool] = mapped_column(default=False)