import re
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, validator, HttpUrl
from strsimpy.jaro_winkler import JaroWinkler
from datetime import datetime

# from src.chat.v1.models import Room

class UserAvatar(BaseModel):
    url: Optional[HttpUrl] = None
    creation_date: datetime = datetime.now()


class User(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = ""
    username: str
    password: str
    # rooms: List[Room] = []
    # image: Optional[UserAvatar] = None
    # bio: Optional[str] = None
    # age: int = 0
    # status: str = ""
    # active: bool = False

    @validator("email")
    def email_validator(cls, v):
        pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not v:
            return v
        if re.match(pattern, v):
            return v
        raise ValueError("not valid email")

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("len needs to be more then 8")
        return v

    @staticmethod
    async def similarity(username:str, password:str):
        jw = JaroWinkler()
        res = jw.similarity(username, password)
        if res <= 0.6:
            return True
        else:
            return False
    
    @staticmethod
    async def validate_login(login: str, db_collection):
        return await db_collection.find_one({"username": login})

    class Config:
        orm_mode = True

class UserDetailData(BaseModel):
    age: int
    status: str

class FriendRequest(BaseModel):
    user_id: str


