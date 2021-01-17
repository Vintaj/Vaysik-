from fastapi import APIRouter

from config.settings import client
from .v1.api import router as v1_router

# Router settings
api_router = APIRouter()


api_router.include_router(v1_router)
