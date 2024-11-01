import pytest
from httpx import AsyncClient, ASGITransport

from core.config import settings
from main import app
from models import User
from tests.utils.utils import get_superuser_token_headers


@pytest.mark.asyncio
async def test_create_notes(test_user: User) -> None:
    data = {"title": "Foo", "content": "Fighters"}
    headers = await get_superuser_token_headers()
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8080",
    ) as client:
        response = await client.post(
            "/api/v1/notes/",
            headers=headers,
            json=data,
        )
    assert response.status_code == 201
