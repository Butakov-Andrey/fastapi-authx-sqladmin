from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/api/v1",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/home", response_class=JSONResponse)
async def home(request: Request) -> JSONResponse:
    return {
        "status": "ok",
        "data": "hello world",
    }
