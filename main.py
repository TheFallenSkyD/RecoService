import logging
from contextlib import asynccontextmanager
from functools import partial

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api_v1.api import api_router
from core.settings import settings
from middleware.auth import JWTAuthBackend, JWTAuthenticationMiddleware
from middleware.exception import json_exceptions_wrapper_middleware
from services.model import ModelService

logger = logging.getLogger("API")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading models started")
    model_service = ModelService()
    app.state.model_service = model_service
    logger.info("Loading models ended")
    yield
    app.state.model_service = None


app = FastAPI(
    title=settings.APP_NAME, description=settings.API_DESCRIPTION, version=settings.API_VERSION, lifespan=lifespan
)

# MIDDLEWARES
app.add_middleware(JWTAuthenticationMiddleware, backend=JWTAuthBackend())
app.middleware("http")(partial(json_exceptions_wrapper_middleware))
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)
# ROUTERS
app.include_router(api_router, prefix="")
