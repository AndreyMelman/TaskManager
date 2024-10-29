from datetime import datetime

import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from crud.tasks import create_task
from models import User
from schemas.task import TaskCreate

from contextlib import nullcontext as does_not_raise


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "title, description, priority, deadline_at, completed, expected",
    [
        (
            "Test Task1",
            "This is a test task",
            "Low",
            "2024-10-25T19:47",
            False,
            does_not_raise(),
        ),
        (
            "Test Task2",
            None,
            "Low",
            "2024-10-25T19:47",
            False,
            does_not_raise(),
        ),
        (
            "Test Task3",
            "This is a test task",
            "Medium",
            "2024-10-25T19:47",
            False,
            does_not_raise(),
        ),
        (
            "Test Task4",
            "This is a test task",
            "Low",
            None,
            False,
            does_not_raise(),
        ),
        (
            "Test Task5",
            "This is a test task",
            "Low",
            "2024-10-25T19:47",
            True,
            does_not_raise(),
        ),
        (
            1,
            "This is a test task",
            "Low",
            "2024-10-25T19:47",
            False,
            pytest.raises(ValueError),
        ),
        (
            "Test Task7",
            1,
            "Low",
            "2024-10-25T19:47",
            False,
            pytest.raises(ValueError),
        ),
        (
            "Test Task8",
            "This is a test task",
            1,
            "2024-10-25T19:47",
            False,
            pytest.raises(ValueError),
        ),
        (
            "Test Task9",
            "This is a test task",
            "Q",
            "2024-10-25T19:47",
            False,
            pytest.raises(ValueError),
        ),
        (
            "Test Task10",
            "This is a test task",
            1,
            "2024-10-25T19:47",
            False,
            pytest.raises(ValueError),
        ),
        (
            "Test Task11",
            "This is a test task",
            False,
            "2024-10-25T19:47",
            False,
            pytest.raises(ValueError),
        ),
        (
            "Test Task12",
            "This is a test task",
            None,
            "2024-10-25T19:47",
            False,
            pytest.raises(ValueError),
        ),
    ],
)
async def test_greate_task(
    session: AsyncSession,
    test_user: User,
    title: str,
    description: str,
    priority: str,
    deadline_at: datetime,
    completed: bool,
    expected,
):
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
