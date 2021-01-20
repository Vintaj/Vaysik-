#!/usr/bin/python3

# system imports
import os
from pathlib import Path


# database imports
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine


# Base App Settings
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Database Settings
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["vaysik"]

user_collection = db["users"]


# Logger Settings
