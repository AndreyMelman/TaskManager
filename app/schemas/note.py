from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteCreate):
    title: str | None = None
    content: str | None = None


class Note(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
    id: int
