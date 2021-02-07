import hashlib
import uuid
from bson import ObjectId


from config.settings import rooms_collection, user_collection, message_collection
from .models import Room, RoomInDB, Message, MessageInDB
from src.user.v1.models import User

async def get_user(name) -> User:
    row = await user_collection.find_one({"username": name})
    if row is not None:
        return User(**row)
    else:
        return None

async def get_userId(userId) -> User:
    row = await user_collection.find_one({"_id": userId})
    if row is not None:
        return User(**row)
    else:
        return None

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

async def get_roomId(roomId) -> RoomInDB:
    row = await rooms_collection.find_one({"_id": ObjectId(roomId)})
    if row is not None:
        return RoomInDB(**row)
    else:
        return None

# Message

async def insert_message(username, content, collection):
    """

        Создание сообщения по id
        
    """

    message = {}
    message["content"] = content
    user = await get_user(username)
    message["user"] = user if user is not None else None
    # room = Room(**room)
    dbmessage = MessageInDB(**message)
    response = await collection.insert_one(dbmessage.dict())
    return {"id_inserted": str(response.inserted_id)}

async def insert_messageId(userId, content, collection):
    """

        Создание сообщения по id пользователя
        
    """

    message = {}
    message["content"] = content
    user = await get_userId(userId)
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

async def send_message(roomId, userId, message):

    """
        
        Основная логика отправки сообщений в комнату.
        
    """


    user = get_userId(userId)
    room = get_roomId(roomId)
    print (f" -- room {room}")
    new_message = message
    await insert_messageId(userId, message, message_collection)
    room_messages = room.messages
    create_message = await rooms_collection.update_one({'_id': ObjectId(roomId)}, {'$set': {'messages': room_messages.append(new_message)}})

    print (" - ")
    print (f" -- user {user}")
    print (f" -- room {room}")
    print (f" -- new_message {new_message}")
    print (f" -- room_messages {room_messages}")
    print (f" -- create_message {create_message}")
    print (" - ")

    return { '201': 'message sending' }