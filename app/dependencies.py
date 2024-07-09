from typing import Annotated

import redis.asyncio as redis
from fastapi import HTTPException, Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db.session_manager import session_manager
from app.redis.cache import PastebinRedis


redis_connection_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
)


async def get_db_session():
    async with session_manager.session() as session:
        yield session


def get_sync_db_session():
    engine = create_engine("postgresql://%s:%s@%s:%s/%s" % (
        settings.DATABASE_USER, settings.DATABASE_PASSWORD,
        settings.DATABASE_HOST, settings.DATABASE_PORT, settings.DATABASE_NAME
    ))
    return sessionmaker(engine)


def get_redis_connection() -> PastebinRedis:
    return PastebinRedis(connection_pool=redis_connection_pool)
