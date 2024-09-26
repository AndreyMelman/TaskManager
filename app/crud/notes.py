from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.engine import Result
from schemas.note import NoteCreate
from models import Note


async def get_notes(
    session: AsyncSession,
) -> list[Note]:
    stmt = select(Note).order_by(Note.id)
    result: Result = await session.execute(stmt)
    notes = result.scalars().all()
    return list(notes)


async def get_note(session: AsyncSession, note_id: int) -> Note | None:
    return await session.get(Note, note_id)


async def create_note(
    session: AsyncSession,
    note_in: NoteCreate,
) -> Note:
    note = Note(**note_in.model_dump())
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note
