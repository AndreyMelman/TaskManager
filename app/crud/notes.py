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


async def get_notes_by_content(
    session: AsyncSession,
    search_query: str,
    limit: int,
    skip: int,
) -> list[Note]:
    stmt = (
        select(Note)
        .where(Note.content.ilike(f"%{search_query}%"))
        .limit(limit)
        .offset(skip)
    )
    result: Result = await session.execute(stmt)
    notes = result.scalars().all()

    return list(notes)


async def get_sorted_notes(
    session: AsyncSession,
    sort_by: str = "created_at",
    order_by: str = "desc",
) -> list[Note]:
    stmt = select(Note)
    if sort_by == "created_at":
        if order_by == "desc":
            stmt = stmt.order_by(Note.created_at.desc())
        else:
            stmt = stmt.order_by(Note.created_at)
    if sort_by == "updated_at":
        if order_by == "desc":
            stmt = stmt.order_by(Note.updated_at.desc())
        else:
            stmt = stmt.order_by(Note.updated_at)

    result: Result = await session.execute(stmt)
    notes = result.scalars().all()
    return list(notes)

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
