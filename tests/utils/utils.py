import string
import random

from main import app
from httpx import AsyncClient, ASGITransport


async def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


async def random_email() -> str:
    return f"{await random_lower_string()}@{await random_lower_string()}.com"


async def get_superuser_token_headers() -> dict[str, str]:

    login_data = {
        "username": "1@1.com",
        "password": "1",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8080",
    ) as client:
        response = await client.post(
            "/api/v1/auth/login",
            data=login_data,
        )
    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
