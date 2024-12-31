from fastapi import FastAPI, Request, Response

from auth.auth_router import auth_router
from Rooms.room_router import room_router
from Comments.comment_router import comment_router

import logging
from config import LOGGER_LEVEL


app = FastAPI(title="Forum Backend")
app.include_router(auth_router, tags=["auth"])
app.include_router(room_router, tags=["rooms"])
app.include_router(comment_router, tags=["comments"])

logging.basicConfig(level=LOGGER_LEVEL, filemode="w")
BaseLogger = logging.getLogger(name="BaseLogger")

# Создаем форматтер и добавляем его в обработчик
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(LOGGER_LEVEL)  # Установка уровня для обработчика


@app.get("/")
async def root():
    BaseLogger.debug("'root' function call")

    return {"message": "Hello World"}
