from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import db_helper
from crud import tasks
from schemas.task import Task, TaskCreate
from deps.dependencies import task_by_id

router = APIRouter(tags=["Tasks"])


@router.get(
    "/",
    response_model=list[Task],
)
async def get_tasks(
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await tasks.get_tasks(session=session)


@router.get(
    "/{task_id}",
    response_model=Task,
)
async def get_task(
    task: Task = Depends(task_by_id),
):
    return task


@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await tasks.create_task(session=session, task_in=task_in)
