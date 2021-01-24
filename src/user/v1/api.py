from common.utils import serialize_to_mongo
from config.settings import user_collection
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.authorization.utils import get_password_hash
from src.authorization.v1.api import get_current_user, oauth2_scheme

from .models import FriendshipRequest, User, UserDetailRequest, UserDetailResponse
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


@router.post("/friend_request/", status_code=status.HTTP_201_CREATED)
async def friend_request(
    user_id: str = Depends(FriendshipRequest), token: str = Depends(oauth2_scheme)
):
    request_data = jsonable_encoder(user_id)
    current_user = await get_current_user(token)

    await user_collection.update_one(
        {"_id": request_data["user_id"]},
        {"$push": {"friend_request.unprocessed_requests": current_user["_id"]}},
    )

    return {"201": "Request Sent"}
