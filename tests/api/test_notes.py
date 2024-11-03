import random

import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from models import User
from tests.utils.note import create_random_note


@pytest.mark.asyncio(loop_scope="session")
async def test_create_notes(
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    data = {"title": "Foo", "content": "Fighters"}
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8080",
    ) as client:
        response = await client.post(
            "/api/v1/notes/",
            headers=superuser_token_headers,
            json=data,
        )
    assert response.status_code == 201
    content = response.json()
    assert content["title"] == data["title"]
    assert content["content"] == data["content"]
    assert "id" in content
    assert "created_at" in content
    assert "updated_at" in content


@pytest.mark.asyncio(loop_scope="session")
async def test_get_note(
    session: AsyncSession,
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    note = await create_random_note(
        session=session,
        superuser=superuser,
    )
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8080",
    ) as client:
        response = await client.get(
            f"/api/v1/notes/{note.id}/",
            headers=superuser_token_headers,
            params={"item_id": note.id},
        )

    assert response.status_code == 200
    content = response.json()
    assert content["title"] == note.title
    assert content["content"] == note.content
    assert content["id"] == note.id
    assert content["user_id"] == superuser.id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_note_not_found(
    session: AsyncSession,
    superuser: User,
    superuser_token_headers: dict[str, str],
):
    note_id = random.randint(1, 100)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8080",
    ) as client:
        response = await client.get(
            f"/api/v1/notes/{note_id}/",
            headers=superuser_token_headers,
            params={"item_id": note_id},
        )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == f"Note {note_id} not found"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_notes(
    session: AsyncSession,
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    await create_random_note(session=session, superuser=superuser)
    await create_random_note(session=session, superuser=superuser)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8080",
    ) as client:
        response = await client.get(
            "/api/v1/notes/",
            headers=superuser_token_headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_get_notes_no_notes(
    session: AsyncSession,
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8080",
    ) as client:
        response = await client.get(
            "/api/v1/notes/",
            headers=superuser_token_headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_update_note(
    session: AsyncSession,
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    note = await create_random_note(
        session=session,
        superuser=superuser,
    )
    data = {"title": "Foo", "content": "Fighters"}
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8080",
    ) as client:
        response = await client.patch(
            f"/api/v1/notes/{note.id}/",
            headers=superuser_token_headers,
            params={"item_id": note.id},
            json=data,
        )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["content"] == data["content"]
    assert content["id"] == note.id
    assert content["user_id"] == superuser.id


@pytest.mark.asyncio(loop_scope="session")
async def test_update_note_not_found(
    session: AsyncSession,
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    note_id = random.randint(1, 100)
    data = {"title": "Foo", "content": "Fighters"}
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8080",
    ) as client:
        response = await client.patch(
            f"/api/v1/notes/{note_id}/",
            headers=superuser_token_headers,
            params={"item_id": note_id},
            json=data,
        )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == f"Note {note_id} not found"


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_note(
    session: AsyncSession,
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    note = await create_random_note(session=session, superuser=superuser)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8080",
    ) as client:
        response = await client.delete(
            f"/api/v1/notes/{note.id}/",
            headers=superuser_token_headers,
            params={"item_id": note.id},
        )
    assert response.status_code == 204


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_note_not_found(
    session: AsyncSession,
    superuser: User,
    superuser_token_headers: dict[str, str],
) -> None:
    note_id = random.randint(1, 100)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8080",
    ) as client:
        response = await client.delete(
            f"/api/v1/notes/{note_id}/",
            headers=superuser_token_headers,
            params={"item_id": note_id},
        )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == f"Note {note_id} not found"
