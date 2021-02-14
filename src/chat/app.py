from fastapi import APIRouter

from config.settings import client
from .v1.chat import router

# Router settings
chat_router = APIRouter()
chat_router.include_router(router)


# Database settings

crud_database = client["crud_db"]
