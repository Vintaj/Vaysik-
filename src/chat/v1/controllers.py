import hashlib
import uuid
import json
from bson import ObjectId


from config.settings import rooms_collection, user_collection, message_collection
from .models import Room, RoomInDB, Message, MessageInDB
from src.user.v1.models import User

async def get_user(name) -> User:
    """

        Найти пользователя по его никнейму
        Search user by her username
        
    """


    row = await user_collection.find_one({"username": name})
    if row is not None:
        return User(**row)
    else:
        return None

async def insert_room(uid, room_name, collection):

    """
    
        Creating room 
        
    """

    room = {} 
    room["room_name"] = room_name
    user = await user_collection.find_one({"_id": uid})

    print('new_user', user)
    room["members"] = [user] if user is not None else []
    # room = Room(**room)
    print("members", room["members"] )
    print('room', room)
    dbroom = RoomInDB(**room)
    print(" dbroom ", dbroom)
    print(" item from members room ", dbroom.members )

    for i in dbroom.members:
        print(i) 


    response = await collection.insert_one(dbroom.dict())
    return {"id_inserted": str(response.inserted_id)}



async def get_rooms():

    """

        Список комнат
        List room
        
    """

    rows = rooms_collection.find()
    row_list = []
    print('--fdsfasda')
    print('rows', rows)
    async for row in rows:
        print('row', row)
        row_list.append(RoomInDB(**row))
    return row_list

async def get_room(room_name) -> RoomInDB:

    """

        Найти комнату по ее названию
        Search room by her name
        
    """


    row = await rooms_collection.find_one({"room_name": room_name})
    if row is not None:
        return RoomInDB(**row)
    else:
        return None

async def get_room_by_id(room_id) -> RoomInDB:

    """

        Найти комнату по ее названию
        Search room by her name
        
    """


    row = await rooms_collection.find_one({"_id": Object(room_id)})
    if row is not None:
        return RoomInDB(**row)
    else:
        return None

async def insert_message(username, content, collection):
    """

        Создание сообщения по id
        Creating message by id
        
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
        Create message by id user
        
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
        
        List message
        Список сообщений

    """

    rows = message_collection.find()
    row_list = []
    async for row in rows:
        row_list.append(MessageInDB(**row))
    return row_list

async def get_message(content) -> MessageInDB:
    """
        
        Search message by content
        Поиск сообщения по контенту

    """

    row = await rooms_collection.find_one({"content": content})
    if row is not None:
        return MessageInDB(**row)
    else:
        return None

async def send_message(data):

    """
        
        Основная логика отправки сообщений в комнату.
        Main logic sending message in room
        Подключить логгирование
        Сделать обработку исключений
        
    """

    message_obj = json.loads(data)
    print( "opa", message_obj )

    username = message_obj.get('user_name')
    print("user_name: ", username)
    room_name = message_obj.get('room_name')
    print("room_name: ", room_name)
    message = message_obj.get('message')
    print("message: ", message)

    user = await user_collection.find_one({"username": username})
    room = await rooms_collection.find_one({"room_name": room_name})

    new_message = message
    insert_messageId(user.get("_id"), message, message_collection)

    create_message = await rooms_collection.update_one(
            {'_id': room.get("_id")}, 
            {'$addToSet': {'messages': new_message}}
        )

    return { '201': 'message sending' }