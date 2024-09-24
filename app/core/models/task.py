from datetime import datetime

from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class Task(Base):

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(15))
    deadline_at: Mapped[datetime]
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )