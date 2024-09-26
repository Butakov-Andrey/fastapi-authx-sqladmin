from authx import TokenPayload
from dependencies import security
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(
    prefix="/api/v1",
    tags=["home"],
    responses={404: {"description": "Not found"}},
)


@router.get("/protected", response_class=JSONResponse)
async def get_protected(
    request: Request,
    payload: TokenPayload = Depends(security.access_token_required),
) -> JSONResponse:
    logger.debug("REFRESH")
    logger.debug(request.cookies.get("refresh_token_cookie"))

    return {
        "email": payload.sub,
        "role": getattr(payload, "role", None),
        "message": "Hello World from protected",
    }
