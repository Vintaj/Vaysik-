from datetime import datetime, timedelta
from typing import Optional

from config.settings import ALGORITHM, SECRET_KEY, user_collection
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str):
    return pwd_context.hash(password)


async def get_user(username: str):
    user = await user_collection.find_one({"username": username})
    return user


async def authenticate_user(username: str, password: str):
    user = await get_user(username)

    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
