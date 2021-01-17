from typing import List, Dict
from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    login: str
    password: str

    class Config:
        orm_mode = True
