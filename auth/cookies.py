from jose import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

from config import JWT_SECRET


DATE_FORMAT = "%H:%M:%S"


class Payload(BaseModel):
    user_id: str
    username: str
    email: str
    expire: str  # datetime вообще


def encode_login_token(user_id: int, username: str, email: str) -> str:
    expire = str(datetime.now() + timedelta(hours=12))
    local_payload = {"user_id": user_id, "username": username, "email": email, "expire": expire}
    token = jwt.encode(local_payload, JWT_SECRET, algorithm="HS256")

    return token


def decode_login_token(token):
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms="HS256")
    decoded_token = Payload(**decoded_token)

    return decoded_token


def is_login_token_valid(token):
    decoded_token: Payload = decode_login_token(token)
    expire = datetime.strptime(decoded_token.expire, DATE_FORMAT)
    if expire >= datetime.now():
        return True
    else:
        return False


def encode_current_room_token(room_id):
    local_payload = {"room_id": room_id}
    token = jwt.encode(local_payload, JWT_SECRET, algorithm="HS256")

    return token


def decode_current_room_token(token):
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms="HS256")

    return decoded_token
