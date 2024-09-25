import sys

from accounts.router import router as accounts_router
from admin import AccountsAdmin, ProfilesAdmin
from config import settings
from dependencies import logging
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
from postgres import engine
from sqladmin import Admin

app = FastAPI(
    title="lms",
    version="0.0.1",
    contact={
        "name": "Andrey Butakov",
        "email": "6669.butakov@gmail.com",
    },
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)
admin = Admin(app, engine)


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
app.include_router(accounts_router, dependencies=[Depends(logging)])
# admin
admin.add_view(AccountsAdmin)
admin.add_view(ProfilesAdmin)
