from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse
router = APIRouter()


@router.get("/", tags=["meta"])
async def root():
    return {"MicroService": "Orchestrator sign process"}


@router.get("/health", tags=["meta"])
async def health_check():
    response = {"satus": "ok"}
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response
    )
