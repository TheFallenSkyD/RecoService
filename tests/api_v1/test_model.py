from unittest.mock import Mock

from httpx import AsyncClient

from exceptions.base import NotFoundError
from services.model import ModelService


async def test_model_success_response(client: AsyncClient):
    response = await client.get("/reco/test/user")
    assert response.status_code == 200, response.json()


async def test_invalid_model_name_422_error(client: AsyncClient):
    response = await client.get("/reco/invalid_model_name/user")
    assert response.status_code == 422, response.json()


async def test_unexciting_model_404_error(client: AsyncClient):
    mocked_model_service = ModelService
    mocked_model_service._get_model_predictions = Mock(side_effect=NotFoundError)
    response = await client.get("/reco/test/user")
    assert response.status_code == 404, response.json()
