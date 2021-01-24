import hashlib
import uuid
from .models import Room, RoomInDB, Message, MessageInDB

# from bson import ObjectId
from config.settings import rooms_collection, user_collection, message_collection
from src.user.v1.models import User

async def get_user(name) -> User:
    row = await user_collection.find_one({"username": name})
    if row is not None:
        return User(**row)
    else:
        return None

# Room

async def insert_room(username, room_name, collection):
    room = {}
    room["room_name"] = room_name
    user = await get_user(username)
    room["members"] = [user] if user is not None else []
    # room = Room(**room)
    dbroom = RoomInDB(**room)
    response = await collection.insert_one(dbroom.dict())
    return {"id_inserted": str(response.inserted_id)}

async def get_rooms():
    rows = rooms_collection.find()
    row_list = []
    async for row in rows:
        row_list.append(RoomInDB(**row))
    return row_list

async def get_room(room_name) -> RoomInDB:
    row = await rooms_collection.find_one({"room_name": room_name})
    if row is not None:
        return RoomInDB(**row)
    else:
        return None

# Message

async def insert_message(username, content, collection):
    """
        
    """

    message = {}
    message["content"] = content
    user = await get_user(username)
    message["user"] = user if user is not None else None
    # room = Room(**room)
    dbmessage = MessageInDB(**message)
    response = await collection.insert_one(dbmessage.dict())
    return {"id_inserted": str(response.inserted_id)}


async def get_messages():
    """
        
    """

    rows = message_collection.find()
    row_list = []
    async for row in rows:
        row_list.append(MessageInDB(**row))
    return row_list

async def get_message(content) -> MessageInDB:
    """
        
    """

    row = await rooms_collection.find_one({"content": content})
    if row is not None:
        return MessageInDB(**row)
    else:
        return None