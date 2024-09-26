from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import db_helper
from crud import tasks
from schemas.task import Task, TaskCreate

router = APIRouter(tags=["Tasks"])


@router.get(
    "/",
    response_model=list[Task],
)
async def get_tasks(
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await tasks.get_tasks(session=session)


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
