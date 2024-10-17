from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from models import Task, User, Category
from schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskUpdateStatus,
)
from models.task import PriorityEnum


async def get_tasks(
    session: AsyncSession,
    user: User,
) -> list[Task]:
    stmt = select(Task).order_by(Task.id).filter(Task.user_id == user.id)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)


async def get_filter_tasks(
    session: AsyncSession,
    priority: PriorityEnum,
    completed: bool,
    user: User,
) -> list[Task]:
    stmt = select(Task).where(Task.user_id == user.id).order_by(Task.id)

    if priority:
        stmt = stmt.where(Task.priority == priority)
    if completed:
        stmt = stmt.where(Task.completed == completed)

    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)


async def get_sorted_tasks(
    session: AsyncSession,
    user: User,
    sort_by: str = "created_at",
    order_by: str = "desc",
) -> list[Task]:
    stmt = select(Task).where(Task.user_id == user.id)
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
    item_id: int,
    user: User,
) -> Task | None:
    stmt = select(Task).where(Task.id == item_id, Task.user_id == user.id)
    result: Result = await session.execute(stmt)
    task = result.scalars().first()
    return task


async def create_task(
    session: AsyncSession,
    task_in: TaskCreate,
    user: User,
) -> Task:
    task = Task(**task_in.model_dump(), user_id=user.id)
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
