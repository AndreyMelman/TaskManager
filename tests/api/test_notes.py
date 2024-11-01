import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from models import User, Note
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
    note = await create_random_note(session=session, superuser=superuser)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8080"
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
