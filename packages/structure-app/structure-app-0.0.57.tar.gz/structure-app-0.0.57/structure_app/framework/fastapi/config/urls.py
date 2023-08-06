from fastapi import APIRouter
from app.api.v1 import views as meta

urls = APIRouter()

urls.include_router(
    meta.router,
    prefix="/api/v1"
)
