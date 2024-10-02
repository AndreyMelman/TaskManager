import enum
from datetime import datetime

from sqlalchemy import String, func, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base
from .mixins.int_id_pk import IntIdPkMixin


class PriorityEnum(str, enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"


class Task(IntIdPkMixin, Base):

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(50000), nullable=True)
    priority: Mapped[PriorityEnum] = mapped_column(
        Enum(PriorityEnum), nullable=True, default=PriorityEnum.medium
    )
    deadline_at: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=datetime.now(),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
