from httpx import AsyncClient


async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200, response.json()


async def test_invalid_auth_token_403_error(client: AsyncClient):
    client.headers.update({"Authorization": "INVALID TOKEN"})
    response = await client.get("/health")
    assert response.status_code == 403, response.json()
