import redis.asyncio as redis

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db.session_manager import session_manager
from app.redis.cache import PastebinRedis


redis_connection_pool = redis.ConnectionPool(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True,
)


async def get_db_session():
    async with session_manager.session() as session:
        yield session


def get_sync_db_session():
    engine = create_engine("postgresql://%s:%s@%s:%s/%s" % (
            settings.database_user, settings.database_password,
            settings.database_host, settings.database_port, settings.database_name
    ))
    return sessionmaker(engine)


def get_redis_connection() -> PastebinRedis:
    return PastebinRedis(connection_pool=redis_connection_pool)
