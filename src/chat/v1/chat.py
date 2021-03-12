from fastapi import APIRouter, FastAPI, WebSocket, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from typing import Optional
from collections import defaultdict
import logging
import pymongo

from .controllers import *
from config.settings import rooms_collection, user_collection, message_collection
from common.utils import serialize_to_mongo
from .models import Room, RoomCreateRequest, MessageCreateRequest
from src.authorization.v1.api import get_current_user, oauth2_scheme

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/v1/chat/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

@router.post("/create_room")
async def create_room(request: RoomCreateRequest):
    print( f'request sosat {request.uid}' )

    res = await insert_room(request.uid, request.room_name, rooms_collection)
    logging.info(f"CREATE_ROOM: room_name: {request.room_name}")
    return {'201': 'room created'}

@router.get("/rooms")
async def rooms(token: str = Depends(oauth2_scheme)):
    current_user = await get_current_user(token)
    user = await user_collection.find({"_id": current_user["_id"]}).to_list(length=None)
    user = user[0]
    rooms = await get_rooms()
    # list_room = [ (i for j in i.members if j.username == user.get('username')) for i in rooms]
    list_room = []
    for i in rooms:
        for j in i.members:
            if j.username == user.get('username'):
                list_room.append(i)
    return list_room 

@router.get("/list_room")
async def list_room(token: str = Depends(oauth2_scheme)):
    rooms = await get_rooms()
    return rooms

@router.get("/room/{room_name}")
async def search_room(room_name, token: str = Depends(oauth2_scheme)):
    room = await get_room(room_name)
    return room

@router.post("/create_message")
async def create_message(request: MessageCreateRequest, token: str = Depends(oauth2_scheme)):
    res = await insert_message(request.username, request.content, message_collection)
    logging.info(f"SEND_MESSAGE: request.username: {request.username}, request.content: {request.content}")
    return {'201': 'room created'}

@router.get("/messages")
async def messages(token: str = Depends(oauth2_scheme)):
    """
        List message  
    """
    messages = await get_messages()
    return messages

@router.get("/")    
async def get():
    return HTMLResponse(html)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):

    """

        Подключение к серверу
        Ендпоинт вебсокета который демонстрирует общение.

        Поменять данный вебсокет именно под комнату для отправки сообщений
    

    """


    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(data, websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
            # await send_message(roomId, userId, message)
            print("data", data)
            await send_message("601ff693fb7694b194f391f5", "601faca84b9a40393eb936db", data)
        
            print(f"You wrote: {data}", websocket)
            print(f"Client #{client_id} says: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
        print(f"Client #{client_id} left the chat")
    except:
        print('Reconnecting')
