from typing import Annotated

from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


async def auth_required(authorization: Annotated[HTTPAuthorizationCredentials, Security(HTTPBearer())]) -> None:
    """
    Просто ставит авторизацию в Swagger.
    Проверка авторизации идет на уровне middleware
    """
    pass
