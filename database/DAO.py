from .database import async_session_maker
from sqlalchemy import insert, update
from sqlalchemy.future import select

from .models import Room, Comment, CommentToComment, User

import logging
from config import LOGGER_LEVEL


DAO_logger = logging.getLogger('BaseLogger.DAOLogger')
DAO_logger.setLevel(LOGGER_LEVEL)


class BaseDAO:
    model = None

    @classmethod
    async def select_all(cls, **values):
        async with async_session_maker() as session:
            DAO_logger.debug(f"Selecting all in {cls.model}")
            result = await session.execute(select(cls.model).filter_by(**values))
            result = result.scalars().all()

        return result

    @classmethod
    async def select_one(cls, **values):
        async with async_session_maker() as session:
            DAO_logger.debug(f"Selecting one in {cls.model}")
            result = await session.execute(select(cls.model).filter_by(**values))
            result = result.fetchone()

        return result

    @classmethod
    async def insert(cls, **values):
        async with async_session_maker() as session:
            try:
                DAO_logger.debug(f"Inserting into {cls.model} values: {values}")
                result = await session.execute(insert(cls.model).values(**values))
                await session.commit()

            except Exception as e:
                DAO_logger.error(f"Failed to insert into {cls.model}: {e}")
                session.rollback()

        return result.inserted_primary_key

    @classmethod
    async def update(cls, mark_id, **new_values):
        async with async_session_maker() as session:
            try:
                DAO_logger.debug(f"Updating mark({mark_id}) in {cls.model} with {new_values}")
                result = await session.execute(update(cls.model).where(cls.model.id == mark_id).values(**new_values))  # noqa
                await session.commit()

            except Exception as e:
                DAO_logger.error(f"Failed to update mark({mark_id}): {e}")
                session.rollback()

        return result.rowcount


class RoomDAO(BaseDAO):
    model = Room

    @classmethod
    async def select_slice(cls, offset: int, limit: int, **values):
        async with async_session_maker() as session:
            DAO_logger.debug(f"Selecting slice in {cls.model}")
            query = select(cls.model).filter_by(**values).offset(offset).limit(limit)
            result = await session.execute(query)
            result = result.scalars().all()

        return result


class CommentDAO(BaseDAO):
    model = Comment


class CommentToCommentDAO(BaseDAO):
    model = CommentToComment


class UserDAO(BaseDAO):
    model = User
