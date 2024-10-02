from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from models import Task
from schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskUpdateStatus,
)
from models.task import PriorityEnum


async def get_tasks(
    session: AsyncSession,
) -> list[Task]:
    stmt = select(Task).order_by(Task.id)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)


async def get_filter_tasks(
    session: AsyncSession,
    priority: PriorityEnum,
    completed: bool,
) -> list[Task]:
    stmt = select(Task).order_by(Task.id)

    if priority:
        stmt = stmt.filter(Task.priority == priority)
    if completed:
        stmt = stmt.filter(Task.completed == completed)

    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)


async def get_sorted_tasks(
    session: AsyncSession,
    sort_by: str = "created_at",
    order_by: str = "desc",
) -> list[Task]:
    stmt = select(Task)
    if sort_by == "deadline_at":
        if order_by == "desc":
            stmt = stmt.order_by(Task.deadline_at.desc())
        else:
            stmt = stmt.order_by(Task.deadline_at)

    if sort_by == "created_at":
        if order_by == "desc":
            stmt = stmt.order_by(Task.created_at.desc())
        else:
            stmt = stmt.order_by(Task.created_at)

    if sort_by == "updated_at":
        if order_by == "desc":
            stmt = stmt.order_by(Task.updated_at.desc())
        else:
            stmt = stmt.order_by(Task.updated_at)

    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)




async def get_task(
    session: AsyncSession,
    task_id: int,
) -> Task | None:
    return await session.get(Task, task_id)


async def create_task(
    session: AsyncSession,
    task_in: TaskCreate,
) -> Task:
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    return task


async def update_task(
    session: AsyncSession,
    task: Task,
    task_update: TaskUpdate,
    partial: bool = False,
) -> Task:
    for name, value in task_update.model_dump(exclude_unset=partial).items():
        setattr(task, name, value)
    await session.commit()
    return task


async def delete_task(
    session: AsyncSession,
    task: Task,
) -> None:
    await session.delete(task)
    await session.commit()


async def mark_task_as_completed(
    session: AsyncSession,
    task_update_status: TaskUpdateStatus,
    task: Task,
) -> Task | None:
    task.completed = task_update_status.completed
    await session.commit()
    return task


async def update_task_priority(
    session: AsyncSession,
    task: Task,
    priority_name: PriorityEnum,
) -> Task:
    task.priority = priority_name

    await session.commit()
    await session.refresh(task)
    return task
