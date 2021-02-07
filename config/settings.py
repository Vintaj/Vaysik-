#!/usr/bin/python3

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# system imports
import os
from pathlib import Path


# database imports
from motor.motor_asyncio import AsyncIOMotorClient


# Base App Settings
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

# Database Settings
client = AsyncIOMotorClient("mongodb://localhost:27017/")


db = client["vaysik"]

user_collection = db["users"]
rooms_collection = db['rooms']
message_collection = db['message']
collect = client["crud_db"]




# Auth Settings
SECRET_KEY = "f0c79a1de9b007c382039f90919ca902be99e56a59891af9a35ee338a1ef578e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

