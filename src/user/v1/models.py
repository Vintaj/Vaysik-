from typing import List, Dict
from pydantic import BaseModel, validator

import re

from config.settings import user_collection


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str

    @validator("email")
    def email_validator(cls, v):
        pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if re.match(pattern, v):
            return v
        raise ValueError("not valid email")

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("len needs to be more then 8")
        return v

    class Config:
        orm_mode = True


class UserDetailRequest(BaseModel):
    login: str


class UserDetailResponse(BaseModel):
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True
