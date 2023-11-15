from exceptions.base import NotFoundError
from schemas.models import ModelNamesEnum, ModelRetrieveSchema


class ModelService:
    async def process_model_response(self, model_name: ModelNamesEnum, user_id: str) -> ModelRetrieveSchema:
        items = self._get_model_predictions(model_name)
        return ModelRetrieveSchema(user_id=user_id, items=items)

    @staticmethod
    def _get_model_predictions(model_name: ModelNamesEnum) -> list[int]:
        match model_name:
            case ModelNamesEnum.TEST:
                return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            case _:
                raise NotFoundError()
