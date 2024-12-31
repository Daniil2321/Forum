from sqlalchemy import Integer, String, Text, Column, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


# Создаем базовый класс для моделей
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class User(BaseModel):
    __tablename__ = 'users'  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор пользователя
    username = Column(String(50), unique=True, nullable=False)  # Имя пользователя
    email = Column(String(100), unique=True, nullable=False)  # Электронная почта
    password = Column(String(100), nullable=False)  # Пароль (обычно хранится в зашифрованном виде)
    bio = Column(Text, nullable=True)  # Биография пользователя (необязательное поле)


class Room(BaseModel):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class Comment(BaseModel):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    comment = Column(Text, nullable=False)
    RoomId = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)


class CommentToComment(BaseModel):
    __tablename__ = 'comments_to_comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    commentId = Column(Integer, ForeignKey('comments.id'), nullable=False)
    comment = Column(Text, nullable=False)
