from typing import Annotated

from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import current_active_user
from core.db import db_helper
from crud import notes
from api.dependencies.note_task_by_id import note_getter
from models import User
from schemas.note import Note, NoteCreate, NoteUpdate

router = APIRouter(
    tags=["Notes"],
)


@router.get(
    "/",
    response_model=list[Note],
)
async def get_notes(
    session: AsyncSession = Depends(db_helper.getter_session),
    user: User = Depends(current_active_user),
):
    return await notes.get_notes(session=session, user=user)


@router.get(
    "/search/",
    response_model=list[Note],
)
async def get_notes_by_content(
    query: Annotated[str, Query()],
    limit: int = 10,
    skip: int = 0,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.getter_session),
):
    note = await notes.get_notes_by_content(
        session=session,
        user=user,
        search_query=query,
        limit=limit,
        skip=skip,
    )
    if not note:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return note


@router.get(
    "/sorted/",
    response_model=list[Note],
)
async def get_sorted_notes(
    sort_by: Annotated[str, Query(enum=["created_at", "updated_at"])] = "created_at",
    order_by: Annotated[str, Query(enum=["asc", "desc"])] = "asc",
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await notes.get_sorted_notes(
        session=session,
        user=user,
        sort_by=sort_by,
        order_by=order_by,
    )


@router.get(
    "/{note_id}/",
    response_model=Note,
)
async def get_note(
    note: Note = Depends(note_getter),
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
    user: User = Depends(current_active_user),
):
    return await notes.create_note(
        session=session,
        note_in=note_in,
        user=user,
    )


@router.patch(
    "/{note_id}/",
    response_model=Note,
)
async def update_note(
    note_update: NoteUpdate,
    note: Note = Depends(note_getter),
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await notes.update_note(
        session=session,
        note=note,
        note_update=note_update,
        partial=True,
    )


@router.delete(
    "/{note_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_note(
    note: Note = Depends(note_getter),
    session: AsyncSession = Depends(db_helper.getter_session),
) -> None:
    return await notes.delete_note(session=session, note=note)
