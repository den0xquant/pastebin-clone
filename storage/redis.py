from loguru import logger

from redis import Redis
from config import base


async def set_key(key: str, value: str) -> None:
    ...


async def get(key):
    ...
