from typing import Annotated

from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.pastes import insert_paste, get_paste_by_hash_id, get_pastes
from app.dependencies import get_db_session, get_redis_connection
from app.models.schemas import APIResponse, CreatePasteSchema
from app.redis.cache import PastebinRedis


async def get_paste(
        paste_hash_id: str,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        rdb: Annotated[PastebinRedis, Depends(get_redis_connection)],
) -> APIResponse:

    cached_paste = await rdb.get_paste_by_hash_id(paste_hash_id)
    if cached_paste:
        return APIResponse(success=True, status_code=status.HTTP_200_OK, response=cached_paste.dict())

    paste = await get_paste_by_hash_id(paste_hash_id, db_session)
    await rdb.incr_paste_views(paste.hash_id)

    return APIResponse(success=True, status_code=status.HTTP_200_OK, response=paste.dict())


async def create_paste(
        data: CreatePasteSchema,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        rdb: Annotated[PastebinRedis, Depends(get_redis_connection)],
) -> APIResponse:

    paste_hash_id = await rdb.lpop(settings.HASH_KEY)
    data.set_hash_id(paste_hash_id)
    paste = await insert_paste(data, db_session)

    await rdb.set_paste_expiration(paste)
    await rdb.set_paste_views(paste_hash_id)

    return APIResponse(
        success=True,
        response=paste.dict(),
        status_code=status.HTTP_201_CREATED
    )


async def fetch_pastes(db_session: Annotated[AsyncSession, Depends(get_db_session)]) -> APIResponse:
    response = await get_pastes(db_session)
    return APIResponse(success=True, response=response, status_code=status.HTTP_200_OK)
