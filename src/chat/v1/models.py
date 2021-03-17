
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, Extra
from datetime import datetime
from bson import ObjectId
from src.user.v1.models import User

class RoomCreateRequest(BaseModel):
    """ Создание румы по апи при запросе
    """

    uid: str
    room_name: str

class MessageCreateRequest(BaseModel):
    username: str
    content: str

class Message(BaseModel):   
    user: User
    content: str = None

class MessageInDB(Message):
    _id: ObjectId
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Room(BaseModel):
    room_name: str  
    members: List[User]
    messages: List[MessageInDB] = []
    last_pinged: datetime = Field(default_factory=datetime.utcnow)




class RoomInDB(Room):
    """

        Рума в базе данных

    """

    _id: ObjectId
    date_created: datetime = Field(default_factory=datetime.utcnow)

