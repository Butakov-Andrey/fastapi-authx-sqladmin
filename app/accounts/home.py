from authx import TokenPayload
from dependencies import security
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/api/v1",
    tags=["home"],
    responses={404: {"description": "Not found"}},
)


@router.get("/protected", response_class=JSONResponse)
async def get_protected(
    payload: TokenPayload = Depends(security.access_token_required),
) -> JSONResponse:
    return {
        "email": payload.sub,
        "role": getattr(payload, "role", None),
        "message": "Hello World from protected",
    }
