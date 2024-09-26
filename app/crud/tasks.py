from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from models import Task
from schemas.task import TaskCreate


async def get_tasks(
    session: AsyncSession,
) -> list[Task]:
    stmt = select(Task).order_by(Task.id)
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)


async def get_task(
    session: AsyncSession,
    task_id: int,
):
    return await session.get(Task, task_id)


async def create_task(
    session: AsyncSession,
    task_in: TaskCreate,
) -> Task:
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
