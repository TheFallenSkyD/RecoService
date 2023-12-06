import logging
from pathlib import Path
from typing import Any

import dill
from rectools.models import PopularModel

from core.settings import settings
from exceptions.base import NotFoundError
from schemas.models import ModelNamesEnum, ModelRetrieveSchema
from services.userknn import UserKnn

logger = logging.getLogger("API")


class ModelService:
    def __init__(self):
        self.models: dict[ModelNamesEnum, Any] = {}
        self.model_ok = False
        self._load_models()

    def _load_models(self):
        try:
            for model_name in (ModelNamesEnum.USER_KNN, ModelNamesEnum.POPULAR):
                if not Path(settings.MODELS_DIRECTORY, f'{model_name.value}.dill').exists():
                    message = f"ML model at {model_name} doesn't exist"
                    logger.error(message)
                    raise FileNotFoundError(message)

                with open(Path(settings.MODELS_DIRECTORY, f'{model_name.value}.dill'), 'rb') as f:
                    model = dill.load(f)

                self.models[model_name] = model
                self.model_ok = True
        except Exception as e:
            logger.error("model loading error", exc_info=e)

    async def process_model_response(self, model_name: ModelNamesEnum, user_id: str) -> ModelRetrieveSchema:
        items = self._get_model_predictions(model_name, user_id)

        if len(items) < 10:
            items += self._get_model_predictions(ModelNamesEnum.POPULAR, user_id)

        items = self._clear_items(items)
        return ModelRetrieveSchema(user_id=user_id, items=items)

    def _get_model_predictions(self, model_name: ModelNamesEnum, user_id: str) -> list[int]:
        if not self.model_ok:
            return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        match model_name:
            case ModelNamesEnum.TEST:
                return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            case ModelNamesEnum.USER_KNN:
                return self.get_user_knn_predictions(user_id)
            case ModelNamesEnum.POPULAR:
                return self.get_popular_predictions()
            case _:
                raise NotFoundError()

    def get_user_knn_predictions(self, user_id: str) -> list[int]:
        model: UserKnn = self.models[ModelNamesEnum.USER_KNN]
        return model.recommend(int(user_id), N_recs=10)

    def get_popular_predictions(self) -> list[int]:
        model: PopularModel = self.models[ModelNamesEnum.POPULAR]
        return list(model.popularity_list[0][:10])

    @staticmethod
    def _clear_items(items: list[int]) -> list[int]:
        return list(dict.fromkeys(items))[:10]
