from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder


from .models import Book


router = APIRouter()


@router.get("/get_all_books/")
async def get_all_books():
    return {"200": "works"}


@router.post("/create_book/", response_model=Book)
async def create_book(book: Book):
    return book


@router.delete("/delete_book/")
async def delete_book():
    return {"201": "Deleted"}
