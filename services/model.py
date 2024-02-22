import logging
from pathlib import Path
from typing import Any

import dill
import numpy as np
import torch
from recbole.model.general_recommender import MultiVAE
from rectools import Columns
from rectools.dataset import Dataset
from rectools.models import PopularModel, ImplicitALSWrapperModel

from core.settings import settings
from exceptions.base import NotFoundError
from schemas.models import ModelNamesEnum, ModelRetrieveSchema
from services.userknn import UserKnn

logger = logging.getLogger("API")


class ModelService:
    def __init__(self):
        self.models: dict[ModelNamesEnum, Any] = {}
        self.model_ok = False
        self.dataset: Dataset | None = None
        self.recbol_dataset: Any | None = None
        self._load_models()

    def _load_models(self):
        try:
            for model_name in (ModelNamesEnum.USER_KNN, ModelNamesEnum.POPULAR, ModelNamesEnum.ASL):
                if not Path(settings.MODELS_DIRECTORY, f"{model_name.value}.dill").exists():
                    message = f"ML model at {model_name} doesn't exist"
                    logger.error(message)
                    raise FileNotFoundError(message)

                with open(Path(settings.MODELS_DIRECTORY, f"{model_name.value}.dill"), "rb") as f:
                    model = dill.load(f)

                self.models[model_name] = model
                self.model_ok = True

            with open(Path(settings.MODELS_DIRECTORY, "dataset.dill"), "rb") as f:
                dataset = dill.load(f)
                self.dataset = dataset

            with open(Path(settings.MODELS_DIRECTORY, "recbol_dataset.dill"), "rb") as f:
                dataset = dill.load(f)
                self.recbol_dataset = dataset
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
            case ModelNamesEnum.ASL:
                return self.get_asl_predictions(user_id)
            case ModelNamesEnum.RECBOLL:
                return self.get_recbol_predictions(user_id)
            case ModelNamesEnum.AUTOENCODER:
                return self.get_autoencoder_predictions(user_id)
            case _:
                raise NotFoundError()

    def get_user_knn_predictions(self, user_id: str) -> list[int]:
        model: UserKnn = self.models[ModelNamesEnum.USER_KNN]
        return model.recommend(int(user_id), N_recs=10)

    def get_asl_predictions(self, user_id: str) -> list[int]:
        model: ImplicitALSWrapperModel = self.models[ModelNamesEnum.ASL]
        return model.recommend([int(user_id)], dataset=self.dataset, k=10, filter_viewed=True)[Columns.Item].tolist()

    def get_popular_predictions(self) -> list[int]:
        model: PopularModel = self.models[ModelNamesEnum.POPULAR]
        return list(model.popularity_list[0][:10])

    @staticmethod
    def _clear_items(items: list[int]) -> list[int]:
        return list(dict.fromkeys(items))[:10]

    def get_recbol_predictions(self, user_id: str) -> list[int]:
        model: MultiVAE = self.models[ModelNamesEnum.RECBOLL]
        with torch.no_grad():
            uid_series = self.recbol_dataset.token2id(self.recbol_dataset.uid_field, [int(user_id)])
            index = np.isin(self.recbol_dataset[self.recbol_dataset.uid_field].numpy(), uid_series)
            new_inter = self.recbol_dataset[index]
            new_inter = new_inter.to("CPU")
            new_scores = model.full_sort_predict(new_inter)
            new_scores[:, 0] = -np.inf
            recommended_item_indices = torch.topk(new_scores, 10).indices[0].tolist()
            recos = self.recbol_dataset.id2token(self.recbol_dataset.iid_field, [recommended_item_indices]).tolist()
        return recos

    def get_autoencoder_predictions(self, user_id: str) -> list[int]:
        model: dict[int, list[int]] = self.models[ModelNamesEnum.AUTOENCODER]
        return model.get(int(user_id), [])
