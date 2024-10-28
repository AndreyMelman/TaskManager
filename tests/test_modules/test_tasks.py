from datetime import datetime

import pytest
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from crud.tasks import create_task
from models import User
from schemas.task import TaskCreate

from contextlib import nullcontext as does_not_raise

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "title, description, priority, deadline_at, completed, expected",
    [
        ("Test Task", "This is a test task", "Low", "2024-10-25T19:47", False, does_not_raise()),
        ("Test Task", None, "Low", "2024-10-25T19:47", False, does_not_raise()),
        ("Test Task", "This is a test task", "Medium", "2024-10-25T19:47", False, does_not_raise()),
        ("Test Task", "This is a test task", "Low", None, False, does_not_raise()),
        ("Test Task", "This is a test task", "Low", "2024-10-25T19:47", True, does_not_raise()),
        (1, "This is a test task", "Low", "2024-10-25T19:47", False, pytest.raises(ValueError)),
        ("Test Task", 1, "Low", "2024-10-25T19:47", False, pytest.raises(ValueError)),
        ("Test Task", "This is a test task", 1, "2024-10-25T19:47", False, pytest.raises(ValueError)),
        ("Test Task", "This is a test task", "Q", "2024-10-25T19:47", False, pytest.raises(ValueError)),
        ("Test Task", "This is a test task", 1, "2024-10-25T19:47", False, pytest.raises(ValueError)),
        ("Test Task", "This is a test task", False, "2024-10-25T19:47", False, pytest.raises(ValueError)),
        ("Test Task", "This is a test task", None, "2024-10-25T19:47", False, pytest.raises(ValueError)),

    ],
)
async def test_greate_task(
    session: AsyncSession,
    title: str,
    description: str,
    priority: str,
    deadline_at: datetime,
    completed: bool,
    expected,
):

    test_user = User(
        email="test@example.com",
        hashed_password="pass",
    )
    session.add(test_user)
    await session.commit()
    await session.refresh(test_user)
    with expected:
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


