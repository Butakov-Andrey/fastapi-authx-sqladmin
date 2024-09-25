import os
from datetime import tzinfo

import pytz
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # OPENROUTER
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    # telegram
    SITE_CONTACTS_BOT: str
    SITE_CONTACTS_GROUP_ID: str = "-1002078876219"

    # timezone
    moscow_timezone: tzinfo = pytz.timezone("Europe/Moscow")

    # logging
    LOGURU_FORMAT: str = "{level}: <level>{message}</level>"

    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE"))


settings = Settings()
