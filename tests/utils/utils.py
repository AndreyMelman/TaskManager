
from httpx import AsyncClient, ASGITransport


from main import app




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
