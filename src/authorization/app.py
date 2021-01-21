from fastapi import APIRouter

from .v1.api import router as v1_router

api_router = APIRouter()

api_router.include_router(v1_router)
