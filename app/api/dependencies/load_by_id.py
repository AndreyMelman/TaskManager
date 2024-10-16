from typing import Annotated, Callable

from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.fastapi_users import current_active_user
from core.db import db_helper
from crud import tasks, notes, categories
from models import Task, Note, User, Category


class LoaderById:
    def __init__(
        self,
        model,
        get_method: Callable,
    ):
        self.model = model
        self.get_method = get_method

    async def __call__(
        self,
        item_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.getter_session),
        user: User = Depends(current_active_user),
    ):

        item = await self.get_method(session=session, item_id=item_id, user=user)
        if item is not None:
            return item
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{self.model.__name__} {item_id} not found",
        )

task_getter = LoaderById(model=Task, get_method=tasks.get_task)
note_getter = LoaderById(model=Note, get_method=notes.get_note)
category_getter = LoaderById(model=Category, get_method=categories.get_category_by_id)


# async def task_by_id(
#     task_id: Annotated[int, Path],
#     session: AsyncSession = Depends(db_helper.getter_session),
# ) -> Task:
#     task = await tasks.get_task(task_id=task_id, session=session)
#     if task is not None:
#         return task
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Task {task_id} not found",
#     )
#
#
# async def note_by_id(
#     note_id: Annotated[int, Path],
#     session: AsyncSession = Depends(db_helper.getter_session),
#     user: User = Depends(current_active_user),
# ) -> Note:
#     note = await notes.get_note(note_id=note_id, session=session, user=user)
#     if note is not None:
#         return note
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Note {note_id} not found",
#     )
