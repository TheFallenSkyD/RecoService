import enum

from pydantic import BaseModel


class ModelNamesEnum(str, enum.Enum):
    TEST = 'test'
    USER_KNN = 'user_knn'
    POPULAR = 'popular'
    ASL = 'asl'


class ModelRetrieveSchema(BaseModel):
    user_id: str
    items: list[int]
