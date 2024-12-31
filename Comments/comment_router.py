from fastapi import APIRouter, Request, Response

from auth.cookies import is_login_token_valid, decode_login_token, decode_current_room_token
from database.DAO import CommentDAO, CommentToCommentDAO
from database.schemas import Comment

import logging
from config import LOGGER_LEVEL


comment_router = APIRouter()

logging.basicConfig(level=LOGGER_LEVEL)
comment_logger = logging.getLogger("BaseLogger.CommentLogger")


@comment_router.post("/create_comment/")
async def create_comment(request: Request, response: Response, comment: Comment):
    token = request.cookies.get("Login_JWT")
    current_room_token = request.cookies.get("current_room_token")
    room_id = decode_current_room_token(current_room_token)["room_id"]


    if not token:
        response.status_code = 401

        return {"message": "Login Required"}

    if not is_login_token_valid(token):
        response.status_code = 401

        return {"message": "Invalid Token"}

    decoded_token = decode_login_token(token)
    await CommentDAO.insert(comment=comment.comment, userId=decoded_token.user_id, roomId=room_id)

    comment_logger.debug(f"Comment created with ID: {comment.id}")

    return {"message": "Comment Created"}
