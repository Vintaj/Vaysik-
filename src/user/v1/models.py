import re
from typing import Optional
from pydantic import BaseModel, validator
from strsimpy.jaro_winkler import JaroWinkler

class User(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = ""
    username: str
    password: str

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


class UserMedia(BaseModel):
    pass


class FriendRequest(BaseModel):
    user_id: str
