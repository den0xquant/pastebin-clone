import http
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, get_redis_connection
from app.models.schemas import APIResponse, CreatePasteSchema
from app.redis.cache import PastebinRedis
from app.service import pastes


router = APIRouter(prefix="/v1/pastes", tags=["pastes"])


@router.get("/test", status_code=http.HTTPStatus.OK)
async def test():
    return {"message": "OK"}


@router.get("/{hash_id}", status_code=http.HTTPStatus.OK, response_model=APIResponse)
async def get_paste(
        hash_id: str,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        rdb: Annotated[PastebinRedis, Depends(get_redis_connection)],
):
    response: APIResponse = await pastes.get_paste(hash_id, db_session, rdb)
    return response


@router.post("/", response_model=APIResponse)
async def create_paste(
        paste: CreatePasteSchema,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        rdb: Annotated[PastebinRedis, Depends(get_redis_connection)]
):
    response: APIResponse = await pastes.create_paste(paste, db_session, rdb)
    return response
