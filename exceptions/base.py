from typing import Any

from fastapi import status


class BaseExceptionMixin(Exception):
    code: int

    def __init__(self, *, message: str = None, data: Any = None):
        self.message = message
        self.data = data


class NotFoundError(BaseExceptionMixin):
    code = status.HTTP_404_NOT_FOUND

    def __init__(self, *, message: str = 'Not Found', data: Any = None):
        super().__init__(message=message, data=data)
