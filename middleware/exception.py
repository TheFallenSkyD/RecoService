import traceback
from typing import Awaitable, Callable

from fastapi.requests import Request
from fastapi.responses import JSONResponse

from exceptions.base import BaseExceptionMixin
from schemas.base import Message


async def json_exceptions_wrapper_middleware(request: Request, call_next: Callable[[Request], Awaitable]):
    """
    JSONResponse exception wrapping
    """
    try:
        return await call_next(request)
    except BaseExceptionMixin as exc:
        return JSONResponse(
            Message(message=exc.message).model_dump(), status_code=exc.code
        )
    except Exception as exc:
        return JSONResponse(
            {"message": f"{exc.__class__.__name__}: {exc}", "traceback": traceback.format_exception(exc)}, 500
        )
