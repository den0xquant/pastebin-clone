import asyncio
import uuid
from datetime import datetime
from random import choice
from string import ascii_letters, digits
from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models import orm
from app.service.auth import get_password_hash


engine = create_async_engine(settings.database_url)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


def generate_random_string(length: int) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))


def generate_user() -> dict[str, Any]:
    return {
        "id": str(uuid.uuid4()),
        "username": generate_random_string(12),
        "email": generate_random_string(12),
        "hashed_password": get_password_hash('secret'),
        "is_active": True,
        "pastes": [],
    }


async def get_user_ids():
    async with async_session() as session:
        result = await session.execute(select(orm.User.id))
        user_ids = [row for row in result.scalars()]
    return user_ids


async def generate_paste() -> dict[str, Any]:
    user_ids = await get_user_ids()
    return {
        "name": generate_random_string(20),
        "text": generate_random_string(200),
        "syntax_highlight": choice([True, False]),
        "exposure": choice([e for e in orm.Exposure]),
        "category": choice([c for c in orm.PasteCategory]),
        "password_disabled": choice([True, False]),
        "password": choice([None, ""]),
        "expiration": choice([e for e in orm.Expiration]),
        "burn_after_read": choice([True, False]),
        "hash_id": generate_random_string(20),
        "user_id": choice(user_ids),
    }


async def insert_users(count: int):
    user_instances = []
    for _ in range(count):
        user = generate_user()
        user_instances.append(user)

    async with async_session() as session:
        await session.execute(insert(orm.User), user_instances)
        await session.commit()


async def insert_pastes(count: int):
    paste_instances = []
    for _ in range(count):
        paste = await generate_paste()
        paste_instances.append(paste)

    async with async_session() as session:
        await session.execute(insert(orm.Paste), paste_instances)
        await session.commit()


async def main():
    await asyncio.gather(insert_users(10))
    await asyncio.gather(insert_pastes(10))


if __name__ == '__main__':
    asyncio.run(main())
