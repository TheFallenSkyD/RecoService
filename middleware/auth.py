import jwt
from fastapi.requests import HTTPConnection
from fastapi.responses import JSONResponse
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthenticationBackend, AuthenticationError
from starlette.middleware.authentication import AuthenticationMiddleware

from core.settings import settings


class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return None

        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            raise AuthenticationError("Not authentication")

        if scheme.lower() != "bearer":
            raise AuthenticationError("Invalid authentication scheme")

        try:
            jwt.decode(credentials, key=settings.SECRET_KEY.get_secret_value(), algorithms=[settings.ALGORITHM],
                       options={"verify_signature": True})
        except Exception:
            raise AuthenticationError("Invalid JWT token")


class JWTAuthenticationMiddleware(AuthenticationMiddleware):
    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=403, content={"detail": str(exc)})
