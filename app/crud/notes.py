from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.note import NoteCreate, NoteUpdate
from models import Note


async def get_notes(
    session: AsyncSession,
) -> list[Note]:
    stmt = select(Note).order_by(Note.id)
    result: Result = await session.execute(stmt)
    notes = result.scalars().all()
    return list(notes)


async def get_note(
    session: AsyncSession,
    note_id: int,
) -> Note | None:
    return await session.get(Note, note_id)


async def create_note(
    session: AsyncSession,
    note_in: NoteCreate,
) -> Note:
    note = Note(**note_in.model_dump())
    session.add(note)
    await session.commit()
    return note


async def update_note(
    session: AsyncSession,
    note: Note,
    note_update: NoteUpdate,
    partial: bool = False,
) -> Note:
    for name, value in note_update.model_dump(exclude_unset=partial).items():
        setattr(note, name, value)
    await session.commit()
    return note


async def delete_note(
    session: AsyncSession,
    note: Note,
) -> None:
    await session.delete(note)
    await session.commit()
