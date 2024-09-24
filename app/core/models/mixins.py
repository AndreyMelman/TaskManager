from datetime import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import mapped_column


class TimestampMixin:

    create_at = Annotated[
        datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
    ]

    update_at = Annotated[
        datetime,
        mapped_column(
            server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.now()
        ),
    ]