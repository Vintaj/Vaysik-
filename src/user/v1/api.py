from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from config.settings import user_collection
from .models import User

from common.utils import serialize_to_mongo

router = APIRouter()


@router.post("/create_user/", response_model=User)
async def create_book(book: User):

    book_data = await serialize_to_mongo(jsonable_encoder(book))
    await user_collection.insert_one(book_data)
    return book
