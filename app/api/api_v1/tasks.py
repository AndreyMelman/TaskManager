from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from .fastapi_users import current_active_user
from core.db import db_helper
from crud import tasks
from api.dependencies.load_by_id import task_getter
from schemas.task import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskUpdateStatus,
    TaskUpdatePriority,
)
from models.task import PriorityEnum


router = APIRouter(tags=["Tasks"])


@router.get("/", response_model=list[Task])
async def get_tasks(
    session: AsyncSession = Depends(db_helper.getter_session),
    user: User = Depends(current_active_user),
):
    return await tasks.get_tasks(session=session, user=user)


@router.get("/filters/", response_model=list[Task])
async def get_filter_tasks(
    priority: Annotated[PriorityEnum, Query(description="Filter by priority")] = None,
    completed: Annotated[bool, Query(description="Filter by completed")] = None,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await tasks.get_filter_tasks(
        session=session,
        priority=priority,
        completed=completed,
        user=user,
    )


@router.get("/sorted/", response_model=list[Task])
async def get_sorted_tasks(
    sort_by: Annotated[str, Query(enum=["deadline_at", "created_at", "updated_at", "category_id",])] = "created_at",
    order_by: Annotated[str, Query(enum=["asc", "desc"])] = "asc",
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await tasks.get_sorted_tasks(
        session=session,
        user=user,
        sort_by=sort_by,
        order_by=order_by,
    )

@router.get('/{category_id}', response_model=list[Task])
async def get_tasks_by_category(
    category_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.getter_session),
    user: User = Depends(current_active_user),
):
    return await tasks.get_tasks_by_category(
        session=session,
        user=user,
        category_id=category_id,
    )


@router.get("/{task_id}/", response_model=Task)
async def get_task(
    task: Task = Depends(task_getter),
):
    return task


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await tasks.create_task(
        session=session,
        task_in=task_in,
        user=user,
    )


@router.patch("/{task_id}/", response_model=Task)
async def update_task(
    task_update: TaskUpdate,
    session: AsyncSession = Depends(db_helper.getter_session),
    task: Task = Depends(task_getter),
):
    return await tasks.update_task(
        session=session,
        task=task,
        task_update=task_update,
        partial=True,
    )


@router.patch("/{task_id}/status/", response_model=TaskUpdateStatus)
async def update_task_status(
    task_update_status: TaskUpdateStatus,
    task: Task = Depends(task_getter),
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await tasks.mark_task_as_completed(
        session=session,
        task=task,
        task_update_status=task_update_status,
    )


@router.patch("/{task_id}/priority/{priority_name}", response_model=TaskUpdatePriority)
async def update_task_priority(
    priority_name: PriorityEnum = Annotated[PriorityEnum, Path(title="Priority Name")],
    task: Task = Depends(task_getter),
    session: AsyncSession = Depends(db_helper.getter_session),
):
    return await tasks.update_task_priority(
        session=session,
        task=task,
        priority_name=priority_name,
    )


@router.delete("/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    session: AsyncSession = Depends(db_helper.getter_session),
    task: Task = Depends(task_getter),
):
    return await tasks.delete_task(
        session=session,
        task=task,
    )
