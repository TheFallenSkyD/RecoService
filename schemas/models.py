import enum

from pydantic import BaseModel


class ModelNamesEnum(str, enum.Enum):
    TEST = 'test'


class ModelRetrieveSchema(BaseModel):
    user_id: str
    items: list[int]
