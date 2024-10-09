from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    title: str = Field(default="", min_length=1, max_length=50)
    content: str = Field(default="", min_length=0, max_length=50000)



class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteCreate):
    title: str | None = Field(default="", max_length=50)
    content: str | None = Field(default="", max_length=50000)


class Note(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
    id: int
    user_id: int
