from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)] = "Title"
    content: Annotated[str | None, Field(min_length=1, max_length=50000)] = None

class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteCreate):
    title: Annotated[str | None, Field(min_length=1, max_length=50)] = None
    content: Annotated[str | None, Field(max_length=50000)] = None


class Note(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
    id: int
    user_id: int
