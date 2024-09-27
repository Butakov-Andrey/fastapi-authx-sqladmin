from authx import TokenPayload
from dependencies import get_session, security
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from models import Account, BlockedRefreshToken
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
def refresh(
    request: Request,
    refresh_payload: TokenPayload = Depends(security.refresh_token_required),
    session: Session = Depends(get_session),
):
    refresh_token = request.cookies.get("refresh_token_cookie")

    block_by_email = BlockedRefreshToken.get_by_email(
        session=session,
        email=refresh_payload.sub,
    )
    block_by_refresh_token = BlockedRefreshToken.get_by_refresh_token(
        session=session,
        refresh_token=refresh_token,
    )

    if block_by_email or block_by_refresh_token:
        raise HTTPException(401, detail={"message": "You are blocked"})

    access_token = security.create_access_token(
        uid=refresh_payload.sub,
        data={"role": getattr(refresh_payload, "role", None)},
    )
    return {"access_token": access_token}
