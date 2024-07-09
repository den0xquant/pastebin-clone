from base64 import b64encode
from random import choice
from string import ascii_letters, digits

import redis
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.dependencies import get_sync_db_session
from app.models.orm import Paste


ASCII_LETTERS_AND_DIGITS = ascii_letters + digits

redis_connection_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
)


def generate_paste_hash() -> str:
    random_string = ''.join([choice(ASCII_LETTERS_AND_DIGITS) for _ in range(62)])
    return b64encode(random_string.encode()).decode('utf-8')[:settings.HASH_LENGTH]


# async def insert_paste_hashes(rdb: redis.Redis):
#     while True:
#         try:
#             keys_count = await rdb.llen(settings.HASH_KEY)
#             if keys_count > settings.HASH_LIMIT:
#                 await rdb.aclose(close_connection_pool=True)
#
#             for _ in range(settings.HASH_COUNT):
#                 await rdb.lpush(settings.HASH_KEY, generate_paste_hash())
#
#             await rdb.aclose(close_connection_pool=True)
#         except RedisError as e:
#             print(e)  # TODO: logging
#             await asyncio.sleep(5)


def paste_delete_handler(message: dict[str, str]):
    if message and message.get('type') == 'pmessage':
        print(f"(PASTE DELETER) Received message: {message}")
        paste_delete_key = message.get('data')

        if not paste_delete_key.startswith(settings.REDIS_DELETE_PREFIX):
            return

        paste_hash_id = paste_delete_key.replace(settings.REDIS_DELETE_PREFIX, "")
        sync_session = get_sync_db_session()

        with sync_session() as session:
            try:
                stmt = select(Paste).filter_by(hash_id=paste_hash_id)
                paste = session.scalars(stmt).first()

                if paste is not None:
                    session.delete(paste)
                    session.commit()

            except SQLAlchemyError as e:
                # TODO: LOGGING
                print(str(e))
                session.rollback()


def main():
    rdb = redis.Redis(connection_pool=redis_connection_pool)
    rdb.config_set('notify-keyspace-events', 'Ex')
    pubsub = rdb.pubsub()
    pubsub.psubscribe(**{"__keyevent@0__:expired": paste_delete_handler})
    pubsub.run_in_thread()


if __name__ == '__main__':
    main()
