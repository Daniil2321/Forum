from fastapi import APIRouter, Response, Request
from sqlalchemy.sql.functions import user

from .cookies import decode_login_token, encode_login_token, is_login_token_valid
from database.DAO import UserDAO
from database.schemas import UserRegister, UserLogin

import logging
from config import LOGGER_LEVEL


auth_router = APIRouter(prefix="/auth", tags=["auth"])

logging.basicConfig(level=LOGGER_LEVEL)
auth_logger = logging.getLogger("BaseLogger.authLogger")


@auth_router.post("/register/")
async def register_user(user: UserRegister):
    current_user = await UserDAO.select_one(email=user.email)

    if not current_user:
        await UserDAO.insert(email=user.email, password=user.password, bio=user.bio, username=user.username)
        auth_logger.debug(f"registered user {user.username} with email {user.email}")

        return {"status": 200, "message": "User registered successfully"}

    return {"status": 400, "message": "User already exists"}


@auth_router.post("/login/")
async def login_user(user: UserLogin, response: Response):
    current_user = await UserDAO.select_one(email=user.email)
    current_user = current_user[0]

    if current_user and current_user.password == user.password:
        token = encode_login_token(username=current_user.username, email=current_user.email, user_id=current_user.id)
        response.set_cookie("Login_JWT", value=token)
        response.status_code = 200
        auth_logger.debug(f"User login as {user.username} with email {user.email}")

        return {"message": "Login Successful"}

    response.status_code = 400

    return {"message": "User does not exist"}


@auth_router.post("/logout/")
async def logout_user(request: Request, response: Response):
    token = request.cookies.get("Login_JWT")

    if token:
        response.delete_cookie("Login_JWT")
        response.status_code = 200
        auth_logger.debug(f"User logout as {user.username} with token {token}")

        return {"message": "Logout Successful"}

    return {"message": "Logout Failed"}


@auth_router.post("/update/")
async def update_user(request: Request, response: Response):
    pass
