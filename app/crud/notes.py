from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from models import Note, User
from schemas.note import NoteCreate, NoteUpdate


async def get_notes(
    session: AsyncSession,
    user: User,
) -> list[Note]:
    stmt = select(Note).where(Note.user_id == user.id).order_by(Note.id)
    result: Result = await session.execute(stmt)
    notes = result.scalars().all()
    return list(notes)


async def get_note(
    session: AsyncSession,
    item_id: int,
    user: User,
) -> Note | None:
    stmt = select(Note).where(
        Note.id == item_id,
        Note.user_id == user.id,
    )
    result = await session.execute(stmt)
    note = result.scalars().first()
    return note


async def get_notes_by_content(
    session: AsyncSession,
    user: User,
    search_query: str,
    limit: int,
    skip: int,
) -> list[Note]:
    stmt = (
        select(Note)
        .where(Note.content.ilike(f"%{search_query}%"), Note.user_id == user.id)
        .limit(limit)
        .offset(skip)
    )
    result: Result = await session.execute(stmt)
    notes = result.scalars().all()

    return list(notes)


async def get_sorted_notes(
    session: AsyncSession,
    user: User,
    sort_by: str = "created_at",
    order_by: str = "desc",
) -> list[Note]:
    stmt = select(Note).where(Note.user_id == user.id)
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
    user: User,
) -> Note:
    note = Note(**note_in.model_dump(), user_id=user.id)
    session.add(note)
    await session.commit()
    await session.refresh(note)
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
