from typing import List, Dict
from pydantic import BaseModel


class Book(BaseModel):
    name: str
    pages: int

    class Config:
        schema_extra = {"name": "book", "pages": 12}


class BookResponse(BaseModel):
    name: str
    pages: int

    class Config:
        schema_extra = {"name": "book", "pages": 12}
