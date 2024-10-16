from datetime import datetime
from typing import Annotated

from sqlalchemy import MetaData, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column

from core.config import settings
from utils.case_converter import camel_case_to_snake_case


created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention
    )

    # Автоматически генерируемое имя таблицы
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"
