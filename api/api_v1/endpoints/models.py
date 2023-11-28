from fastapi import APIRouter, status
from fastapi.requests import Request

from schemas.base import Error, Message
from schemas.models import ModelNamesEnum, ModelRetrieveSchema
from services.model import ModelService

router = APIRouter()


@router.get(
    "/{model_name}/{user_id}",
    response_model=ModelRetrieveSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": Error,
            "description": "Not enough privileges",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": Message,
            "description": "Model was not found",
        },
    },
)
async def get_model_response(request: Request, model_name: ModelNamesEnum, user_id: str):
    service: ModelService = request.app.state.model_service
    return await service.process_model_response(model_name, user_id)
