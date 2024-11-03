import random

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from models import User
from models.task import PriorityEnum
from tests.utils.task import create_random_task


@pytest.mark.asyncio(loop_scope="session")
async def test_create_task(
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    data = {
        "title": "Foo",
        "description": "Fighters",
        "priority": "Low",
        "deadline_at": "2024-11-03T12:59:31",
        "completed": False,
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as client:
        response = await client.post(
            "/api/v1/tasks/",
            headers=superuser_token_headers,
            json=data,
        )
    assert response.status_code == 201
    content = response.json()
    assert content["title"] == "Foo"
    assert content["description"] == "Fighters"
    assert content["priority"] == "Low"
    assert content["completed"] is False
    assert content["deadline_at"] == "2024-11-03T12:59:31"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_task(
    session: AsyncSession,
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    task = await create_random_task(
        session=session,
        superuser=superuser,
    )
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        response = await client.get(
            f"/api/v1/tasks/{task.id}/",
            headers=superuser_token_headers,
            params={"item_id": task.id},
        )

    assert response.status_code == 200
    content = response.json()
    assert content["title"] == task.title
    assert content["description"] == task.description
    assert content["priority"] == task.priority
    assert content["completed"] == task.completed
    assert content["deadline_at"] == task.deadline_at.isoformat()
    assert content["id"] == task.id
    assert content["user_id"] == superuser.id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_tasks(
    session: AsyncSession,
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    await create_random_task(
        session=session,
        superuser=superuser,
    )
    await create_random_task(
        session=session,
        superuser=superuser,
    )
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        response = await client.get(
            "/api/v1/tasks/",
            headers=superuser_token_headers,
        )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 1


@pytest.mark.asyncio(loop_scope="session")
async def test_update_task(
    session: AsyncSession,
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    task = await create_random_task(
        session=session,
        superuser=superuser,
    )
    data = {
        "title": "Title",
        "description": "Description",
        "priority": PriorityEnum.low,
    }
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        response = await client.patch(
            f"/api/v1/tasks/{task.id}/",
            headers=superuser_token_headers,
            params={"item_id": task.id},
            json=data,
        )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["id"] == task.id
    assert content["user_id"] == superuser.id


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_task(
    session: AsyncSession,
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    task = await create_random_task(
        session=session,
        superuser=superuser,
    )
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        response = await client.delete(
            f"/api/v1/tasks/{task.id}/",
            headers=superuser_token_headers,
            params={"item_id": task.id},
        )
    assert response.status_code == 204
