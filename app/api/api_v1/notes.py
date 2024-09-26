from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from crud import notes
from core.db import db_helper
from schemas.note import Note, NoteCreate
from deps.dependencies import note_by_id

router = APIRouter(tags=["Notes"])


@router.get(
    "/",
    response_model=list[Note],
)
async def get_notes(
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await notes.get_notes(session=session)


@router.get(
    "/{note_id}",
    response_model=Note,
)
async def get_note(
    note: Note = Depends(note_by_id),
):
    return note


@router.post(
    "/",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
    note_in: NoteCreate,
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await notes.create_note(session=session, note_in=note_in)
