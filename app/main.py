import sys

from accounts.auth import router as auth_router
from accounts.home import router as home_router
from admin import AccountsAdmin, BlockedRefreshTokensAdmin, ProfilesAdmin
from authx import AuthX
from config import settings
from dependencies import logging
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
from postgres import engine
from sqladmin import Admin

# main
app = FastAPI(
    title="lms",
    contact={
        "name": "Andrey Butakov",
        "email": "6669.butakov@gmail.com",
    },
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# admin
admin = Admin(app, engine)

# authx handle errors
AuthX().handle_errors(app)

# static
app.mount("/static", StaticFiles(directory="static"), name="static")

# logger
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format=settings.LOGURU_FORMAT,
)


# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(auth_router, dependencies=[Depends(logging)])
app.include_router(home_router, dependencies=[Depends(logging)])
# admin
admin.add_view(AccountsAdmin)
admin.add_view(ProfilesAdmin)
admin.add_view(BlockedRefreshTokensAdmin)
