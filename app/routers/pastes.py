import http
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, get_redis_connection
from app.models.schemas import APIResponse, CreatePasteSchema, PasteSchema
from app.redis.cache import PastebinRedis
from app.service import pastes


router = APIRouter(prefix="/pastes", tags=["pastes"])


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


@router.get("/", response_model=APIResponse)
async def list_pastes(db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    response: APIResponse = await pastes.fetch_pastes(db_session)
    return response
