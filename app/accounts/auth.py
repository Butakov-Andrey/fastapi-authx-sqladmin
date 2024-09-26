from authx import TokenPayload
from dependencies import get_session, security
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger
from models import Account
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.get("/login", response_class=JSONResponse)
async def login(
    request: Request,
    email: str,
    password: str,
    session: Session = Depends(get_session),
) -> JSONResponse:
    account = Account.get_by_email(session, email)
    if not account or not bcrypt.verify(password, account.password_hash):
        raise HTTPException(401, detail={"message": "Bad credentials"})

    # получаем роль и записываем в payload
    access_token = security.create_access_token(
        uid=email,
        data={"role": account.role.value},
    )
    refresh_token = security.create_refresh_token(
        uid=email,
        data={"role": account.role.value},
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/refresh")
def refresh(refresh_payload: TokenPayload = Depends(security.refresh_token_required)):
    # TODO: проверять, есть ли в базе refresh token или email

    logger.debug("REFRESH")

    access_token = security.create_access_token(refresh_payload.sub)
    return {"access_token": access_token}
