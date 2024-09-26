from datetime import timedelta

from authx import AuthX, AuthXConfig
from config import settings
from fastapi import Request
from loguru import logger
from postgres import SessionLocal

# authx JWT
auth_config = AuthXConfig()
auth_config.JWT_ALGORITHM = "HS256"
auth_config.JWT_SECRET_KEY = settings.SECRET_KEY
auth_config.JWT_TOKEN_LOCATION = ["cookies"]
auth_config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
auth_config.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
security = AuthX(config=auth_config)


# database dependency
async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# logger
def logging(request: Request):
    logger.debug("~~~ Request:")
    logger.debug(f"{request.method} {request.url}")
    logger.debug("Params:")
    for name, value in request.path_params.items():
        logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    logger.debug(f"host: {request.headers.get('host')}")
