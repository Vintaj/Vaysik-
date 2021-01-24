
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from src.user.v1.models import User

class RoomCreateRequest(BaseModel):
    username: str
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
    members: Optional[List[User]] = []
    messages: Optional[List[MessageInDB]] = []
    last_pinged: datetime = Field(default_factory=datetime.utcnow)


class RoomInDB(Room):
    _id: ObjectId
    date_created: datetime = Field(default_factory=datetime.utcnow)

