from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    username: str
    password: str
    bio: str


class UserLogin(BaseModel):
    email: str
    password: str


class Room(BaseModel):
    title: str
    content: str
    ownerId: int
    creatorId: int


class Comment(BaseModel):
    comment: str
    RoomId: int
    UserId: int


class CommentToComment(BaseModel):
    commentId: int
    comment: str
