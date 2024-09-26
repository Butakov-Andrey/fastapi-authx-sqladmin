from authx import TokenPayload
from dependencies import security
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger

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
) -> JSONResponse:
    # TODO
    # пробуем найти пользователя по email в базе
    # 422
    # {
    #     "message": "Invalid Token",
    #     "error_type": "JWTDecodeError"
    # }
    # сверяем его пароль
    # получаем роль и записываем в payload
    if email == "test" and password == "test":
        access_token = security.create_access_token(
            uid=email,
            data={"role": "ADMIN"},
        )
        refresh_token = security.create_refresh_token(
            uid=email,
            data={"role": "ADMIN"},
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    raise HTTPException(401, detail={"message": "Bad credentials"})


@router.post("/refresh")
def refresh(refresh_payload: TokenPayload = Depends(security.refresh_token_required)):
    # TODO: проверять, есть ли в базе refresh token или email

    logger.debug("REFRESH")

    access_token = security.create_access_token(refresh_payload.sub)
    return {"access_token": access_token}
