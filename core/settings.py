from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Reco Service"
    API_VERSION: str = "production"
    API_DESCRIPTION: str = "Reco Service For AI Talent Hub"

    DEBUG: bool = False

    CORS_ALLOW_HEADERS: list[str] = ["*"]
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_ORIGINS: list[str] = ["*"]

    SECRET_KEY: SecretStr = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"


settings = Settings()
