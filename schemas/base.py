from pydantic import BaseModel


class Message(BaseModel):
    message: str


class Error(BaseModel):
    detail: str
