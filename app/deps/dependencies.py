from typing import Annotated

from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.db import db_helper
from crud import tasks, notes


async def task_by_id(
    task_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.getter_session),
):
    task = await tasks.get_task(task_id=task_id, session=session)
    if task is not None:
        return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found",
    )


async def note_by_id(
    note_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.getter_session),
):
    task = await notes.get_note(note_id=note_id, session=session)
    if task is not None:
        return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {note_id} not found",
    )
