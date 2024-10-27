from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from crud.tasks import create_task
from models import User
from schemas.task import TaskCreate


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "title, description, priority, deadline_at, completed",
    [
        ("Test Task", "This is a test task", "Low", "2024-10-25T19:47", False),
        ("Test Task1", "This is a test task", "Low", "2024-10-25T19:47", False),
        ("Test Task2", None, "Low", "2024-10-25T19:47", False),
    ],
)
async def test_greate_task(
    session: AsyncSession,
    title: str,
    description: str,
    priority: str,
    deadline_at: datetime,
    completed: bool,
):

    test_user = User(
        email=f"test_{title.replace(' ', '_').lower()}@example.com",
        hashed_password="pass",
    )
    session.add(test_user)
    await session.commit()
    # await session.refresh(test_user)

    task_data = TaskCreate(
        title=title,
        description=description,
        priority=priority,
        deadline_at=deadline_at,
        completed=completed,
    )

    new_task = await create_task(session=session, task_in=task_data, user=test_user)

    assert new_task.id is not None
    assert new_task.title == task_data.title
    assert new_task.description == task_data.description
    assert new_task.priority == task_data.priority
    assert new_task.deadline_at == task_data.deadline_at
    assert new_task.completed == task_data.completed
    assert new_task.user_id == test_user.id


