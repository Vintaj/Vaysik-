from fastapi import APIRouter, FastAPI, WebSocket, Request, Depends
from fastapi.encoders import jsonable_encoder
from typing import Optional
from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, status
from fastapi.responses import HTMLResponse
from collections import defaultdict
import logging
from fastapi.templating import Jinja2Templates
# from .mongodb import close_mongo_connection, connect_to_mongo, get_nosql_db, AsyncIOMotorClient
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
# from .config import MONGODB_DB_NAME
from .controllers import insert_room, get_rooms, insert_message, get_room, get_messages
from starlette.websockets import WebSocket, WebSocketDisconnect
import pymongo

from config.settings import rooms_collection, user_collection, message_collection

from .models import Room, RoomCreateRequest, MessageCreateRequest

# var ws = new WebSocket("ws://localhost:8000/v1/chat/ws");
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



# Room -----------------------
@router.post("/create_room")
async def create_room(request: RoomCreateRequest, token: str = Depends(oauth2_scheme)):
    """
        Create room  
    """
    res = await insert_room(request.username, request.room_name, rooms_collection)
    return {'201': 'room created'}

@router.get("/rooms")
async def rooms(token: str = Depends(oauth2_scheme)):
    """
        List room  
    """
    rooms = await get_rooms()
    return rooms

@router.get("/room/{room_name}")
async def search_room(room_name, token: str = Depends(oauth2_scheme)):
    """
        Search room  
    """

    room = await get_room(room_name)
    return room

# Message ---------------------------
@router.post("/create_message")
async def create_message(request: MessageCreateRequest, token: str = Depends(oauth2_scheme)):
    res = await insert_message(request.username, request.content, message_collection)
    return {'201': 'room created'}

@router.get("/messages")
async def messages(token: str = Depends(oauth2_scheme)):
    """
        List message  
    """
    messages = await get_messages()
    return messages

# WebSocket ---------------------------------------------

@router.get("/")    
async def get():
    return HTMLResponse(html)

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    # Подключение к серверу
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")