from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from crud import notes
from core.db import db_helper
from schemas.note import Note, NoteCreate, NoteUpdate
from deps.dependencies import note_by_id

router = APIRouter(tags=["Notes"])


@router.get("/", response_model=list[Note])
async def get_notes(
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await notes.get_notes(session=session)


@router.get("/{note_id}/", response_model=Note)
async def get_note(
    note: Note = Depends(note_by_id),
):
    return note


@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_in: NoteCreate,
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await notes.create_note(session=session, note_in=note_in)


@router.patch("/{note_id}/", response_model=Note)
async def update_note(
    note_update: NoteUpdate,
    note: Note = Depends(note_by_id),
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await notes.update_note(
        session=session,
        note=note,
        note_update=note_update,
        partial=True,
    )


@router.delete("/{note_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note: Note = Depends(note_by_id),
    session: AsyncSession = Depends(db_helper.getter_session),
) -> None:
    return await notes.delete_note(session=session, note=note)
