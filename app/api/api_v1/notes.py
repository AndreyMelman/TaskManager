from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from crud import notes
from core.db import db_helper
from schemas.note import Note, NoteCreate

router = APIRouter(tags=["Notes"])


@router.get(
    "/",
    response_model=list[Note],
)
async def get_notes(session: AsyncSession = Depends(db_helper.getter_session)):
    return await notes.get_notes(session=session)


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
