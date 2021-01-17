from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from src.crud.app import api_router as v1_crud_router


# App Settings
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"], include_in_schema=False)
async def health_check():
    return {"status": "ok"}


# Router Settings

app.include_router(v1_crud_router, prefix="/v1")
