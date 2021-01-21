from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder

from config.settings import user_collection
from src.authorization.utils import get_password_hash

from .models import User, UserDetailRequest, UserDetailResponse

from common.utils import serialize_to_mongo
from .validators import validate_login

router = APIRouter()


@router.post("/create_user/", response_model=User)
async def create_user(user: User):
    request_data = await serialize_to_mongo(jsonable_encoder(user))

    if not await validate_login(request_data["username"]):
        request_data["hashed_password"] = await get_password_hash(
            request_data["password"]
        )
        await user_collection.insert_one(request_data)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Login Exists"
        )


@router.get("/get_user_data/{username}", response_model=UserDetailResponse)
async def get_user_detail(username: str = Depends(UserDetailRequest)):
    request_data = jsonable_encoder(username)

    data = await user_collection.find_one({"username": request_data["username"]})
    return data


@router.get("/get_all_users/")
async def get_all_users():

    users_data = await user_collection.find(
        {}, {"_id": 0, "first_name": 1, "last_name": 1, "email": 1}
    ).to_list(length=None)

    return users_data


@router.get("/items/")
async def read_items(q: Optional[str] = None):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result
