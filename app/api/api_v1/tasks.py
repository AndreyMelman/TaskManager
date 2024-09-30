from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import db_helper
from crud import tasks
from schemas.task import Task, TaskCreate, TaskUpdate
from deps.dependencies import task_by_id

router = APIRouter(tags=["Tasks"])


@router.get("/", response_model=list[Task])
async def get_tasks(
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await tasks.get_tasks(session=session)


@router.get("/{task_id}/", response_model=Task)
async def get_task(
    task: Task = Depends(task_by_id),
):
    return task


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await tasks.create_task(
        session=session,
        task_in=task_in,
    )


@router.patch("/{task_id}/", response_model=Task)
async def update_task(
    task_update: TaskUpdate,
    session: AsyncSession = Depends(db_helper.getter_session),
    task: Task = Depends(task_by_id),
):
    return await tasks.update_task(
        session=session,
        task=task,
        task_update=task_update,
        partial=True,
    )


@router.delete("/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    session: AsyncSession = Depends(db_helper.getter_session),
    task: Task = Depends(task_by_id),
):
    return await tasks.delete_task(
        session=session,
        task=task,
    )
