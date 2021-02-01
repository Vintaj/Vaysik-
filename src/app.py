from fastapi import APIRouter

from config.settings import app
from src.user.app import api_router as v1_user_router
from src.authorization.app import api_router as v1_auth_router


# App Settings


@app.get("/health", tags=["health"], include_in_schema=False)
async def health_check():
    return {"status": "ok"}


# Router Settings

app.include_router(v1_user_router, prefix="/v1/user")
app.include_router(v1_auth_router, prefix="/auth")
