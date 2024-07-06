from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select, insert, exists
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.dependencies import get_db_session, get_redis_connection
from app.models.orm import Paste
from app.models.schemas import APIResponse, APIError, PasteSchema, CreatePasteSchema
from app.redis.cache import PastebinRedis, get_views_key


async def incr_views(rdb: PastebinRedis, paste: PasteSchema):
    await rdb.incr(get_views_key(paste.hash_id))
    views = await rdb.get(get_views_key(paste.hash_id))
    if int(views) >= settings.REDIS_VIEWS_TO_CACHE:
        await rdb.set_paste_cache(paste)


async def get_paste(
        paste_hash_id: str,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        rdb: Annotated[PastebinRedis, Depends(get_redis_connection)],
) -> APIResponse:
    response_dict = {'success': True, 'response': {}, 'status_code': HTTPStatus.OK, 'error': None}

    cached_paste = await rdb.get_paste_by_hash_id(paste_hash_id)
    if cached_paste:
        response_dict['response'] = cached_paste.dict()
        return APIResponse(**response_dict)

    try:
        stmt = select(Paste).where(paste_hash_id == Paste.hash_id)
        paste_orm = (await db_session.scalars(stmt)).first()

        if paste_orm is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not found')

        paste = PasteSchema.from_orm(paste_orm)
        await db_session.commit()
        response_dict['response'] = paste.dict()

    except SQLAlchemyError as e:
        response_dict['error'] = APIError(code=e.code, message=e.__class__.__name__)
        return APIResponse(**response_dict)

    await incr_views(rdb, paste)

    return APIResponse(**response_dict)


async def create_paste(
        create_paste_data: CreatePasteSchema,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        rdb: Annotated[PastebinRedis, Depends(get_redis_connection)]
) -> APIResponse:
    stmt = select(exists().where(create_paste_data.name == Paste.name))
    is_existed = await db_session.scalar(stmt)

    if is_existed:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Paste already exists')

    try:
        paste_hash_id = await rdb.lpop(settings.HASH_KEY)
        create_paste_data.set_hash_id(paste_hash_id)
        result = await db_session.scalar(insert(Paste).values(create_paste_data.dict()).returning(Paste))
        paste = PasteSchema.from_orm(result)
        await db_session.commit()
        await rdb.set_paste_expiration(paste)
        await rdb.set(get_views_key(paste_hash_id), 0)

    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Paste cannot be created'
        )

    return APIResponse(success=True, response=create_paste_data.dict(), status_code=HTTPStatus.CREATED)
