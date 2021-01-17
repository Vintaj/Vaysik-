from fastapi import APIRouter

from config.settings import client
from .v1.api import router

# Router settings
api_router = APIRouter()
api_router.include_router(router)


# Database settings

crud_database = client["crud_db"]
