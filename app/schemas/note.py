from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    title: str
    content: str


class CreateNote(NoteBase):
    pass


class UpdateNote(CreateNote):
    pass


class UpdateNotePartial(CreateNote):
    title: str | None = None
    content: str | None = None


class Note(NoteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
