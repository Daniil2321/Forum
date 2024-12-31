from fastapi import APIRouter, Request, Response

from database.DAO import RoomDAO
from database.schemas import Room
from auth.cookies import is_login_token_valid, decode_login_token, encode_current_room_token

import logging
from config import LOGGER_LEVEL


room_router = APIRouter()

logging.basicConfig(level=LOGGER_LEVEL)
room_logger = logging.getLogger("BaseLogger.RoomLogger")


@room_router.get("/rooms/{offset}/{limit}")
async def get_rooms(offset: int, limit: int):
    rooms = await RoomDAO.select_slice(offset=offset, limit=limit)
    room_logger.debug(f"Rooms selected: {rooms}")

    return {"rooms": rooms}


@room_router.get("/room/{room_id}")
async def get_room(room_id: int, response: Response):
    room = await RoomDAO.select_one(room_id=room_id)

    if not room:
        return {"message": "Room not found"}

    current_room_token = encode_current_room_token(room_id)
    response.set_cookie(key="room_id", value=current_room_token)

    room_logger.debug(f"Room ID: {room_id}, Current Room Token: {current_room_token}")

    return {"room": room}


@room_router.post("/create_room/")
async def create_room(request: Request, room: Room, response: Response):
    token = request.headers.get("Login_LWT")

    if not token:
        response.status_code = 401

        return {"message": "Login required"}

    if not is_login_token_valid(token):
        response.status_code = 401

        return {"message": "Invalid token"}

    decoded_token = decode_login_token(token)
    room_id = await RoomDAO.insert(
        title=room.title,
        content=room.content,
        creator_id=decoded_token.id,
        owner_id=decoded_token.owner_id
    )
    room_logger.debug(f"room created with ID: {room_id}")

    response.status_code = 200

    return {"message": "Room created", "room_id": room_id}
