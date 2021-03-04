from typing import List
from common.utils import serialize_to_mongo
from config.settings import user_collection
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.authorization.utils import get_password_hash
from src.authorization.v1.api import get_current_user, oauth2_scheme

from .models import FriendRequest, User
from .validators import validate_login
from datetime import datetime


router = APIRouter()


@router.get("/me/")
async def get_me(token: str = Depends(oauth2_scheme)):
    print("token: ", token)
    print("function begin")
    current_user = await get_current_user(token)
    print("current_user", current_user)
    return await user_collection.find({"_id": current_user["_id"]}).to_list(length=None)


@router.post("/create_user/", response_model=User)
async def create_user(user: User) -> List[dict]:
    """
        Creates a user and save into DB
    """
    request_data = await serialize_to_mongo(jsonable_encoder(user))


    if  not await User.similarity(request_data["username"], request_data["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is to similarity"
        )
    if not await User.validate_login(request_data["username"], user_collection):
        request_data["hashed_password"] = await get_password_hash(
            request_data["password"]
        )
        request_data.pop("password", None)
        request_data["created_at"] = datetime.now()
        await user_collection.insert_one(request_data)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Login Exists"
        )

@router.get("/get_one/")
async def get_user_username(username: str) -> List[dict]:
    """
        Returns one users depends on username
    """
    request_data = jsonable_encoder(username)
    print("username", username)
    data = await user_collection.find(
        {"username": request_data},
        {"_id": 0, "first_name": 1, "last_name": 1, "email": 1},
    ).to_list(length=None)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="UserNotFound"
        )
    return data

@router.get("/detail_user/")
async def get_user_detail(username: str) -> List[dict]:
    """
        Returns user detail
    """
    current_user = await get_current_user(token)
    return {"200": "success"}

@router.get("/user_update/")
async def user_update(username: str) -> List[dict]:
    """
        Returns user detail
    """
    current_user = await get_current_user(token)
    
    return {"200": "success"}


@router.get("/get_all/")
async def get_all_users() -> List[dict]:
    """
        PROCESS:
            return all users
    """

    users_data = await user_collection.find(
        {}, {"_id": 0, "first_name": 1, "last_name": 1, "email": 1}
    ).to_list(length=None)

    return users_data if len(users_data) > 0 else []


@router.post("/friend/request/", status_code=status.HTTP_201_CREATED)
async def friend_request(
    user_id: str = Depends(FriendRequest), token: str = Depends(oauth2_scheme)
) -> None:

    """
        PROCESS:
            add requestor id to requested_user friends request
            if requested user exists and has no requests from requestor
    """

    request_data = jsonable_encoder(user_id)
    current_user = await get_current_user(token)

    if not await user_collection.find_one({"_id": request_data["user_id"]}):
        return {"404": "UserNotFound"}

    if not await user_collection.find_one(
        {
            "_id": request_data["user_id"],
            "friend_request.unprocessed_requests": {"$in": [current_user["_id"]]},
        }
    ):
        if current_user['_id'] == request_data["user_id"]:

            return {"404": "SameAsSenderID"}

        await user_collection.update_one(

            {"_id": request_data["user_id"]},
            {"$push": {"friend_request.unprocessed_requests": current_user["_id"]}},
        )
        return {"201": "RequestSent"}

    return {"401": "Request Already Been Sent"}


@router.put("/friend/apply", status_code=status.HTTP_200_OK)
async def friend_request_apply(
    user_id: str = Depends(FriendRequest), token: str = Depends(oauth2_scheme)
) -> None:

    """
        PROCESS:
            Apply friendship request
    """
    request_data = jsonable_encoder(user_id)
    current_user = await get_current_user(token)

    if not await user_collection.find_one({"_id": request_data["user_id"]}):
        return {"404": "UserNotFound"}

    await user_collection.update_one(
        {"_id": current_user["_id"]},
        {
            "$push": {"friend_request.applied_requests": request_data["user_id"]},
            "$pull": {"friend_request.unprocessed_requests": request_data["user_id"]},
        },
    )

    return {"201": "RequestApplied"}


@router.put("/friend/decline", status_code=status.HTTP_200_OK)
async def friend_request_decline(
    user_id: str = Depends(FriendRequest), token: str = Depends(oauth2_scheme)
) -> None:
    """
        PROCESS:
            Decline friendship request
    """
    request_data = jsonable_encoder(user_id)
    current_user = await get_current_user(token)

    if not await user_collection.find_one({"_id": request_data["user_id"]}):
        return {"404": "UserNotFound"}

    await user_collection.update_one(
        {"_id": current_user["_id"]},
        {
            "$push": {"friend_request.declined_requests": request_data["user_id"]},
            "$pull": {"friend_request.unprocessed_requests": request_data["user_id"]},
        },
    )

    return {"201": "RequestDeclined"}

@router.get('/friend/counter', status_code=status.HTTP_200_OK)
async def friend_request_counter(user_id: str) -> List[dict]:
    """
        PROCESS:
            Shows requests count
    """
    request_data = jsonable_encoder(user_id)
    count = await user_collection.find_one({
        "_id": request_data,
        "friend_request.unprocessed_request": {"$ne": True},
    })
    if not await user_collection.find_one({"_id": request_data}):
        return {"404": "UserNotFound"}

    return {"200": len(
        count['friend_request']['unprocessed_requests']
    )}
