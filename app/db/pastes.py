from fastapi import HTTPException, status
from sqlalchemy import select, exists, insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas import PasteSchema, CreatePasteSchema
from app.models.orm import Paste


async def check_paste_existing(name: str, db_session: AsyncSession) -> bool:
    stmt = select(exists().where(name == Paste.name))
    is_existed = await db_session.scalar(stmt)
    return is_existed


async def insert_paste(data: CreatePasteSchema, db_session: AsyncSession) -> PasteSchema | None:
    is_paste_existed = await check_paste_existing(data.name, db_session)
    if is_paste_existed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Paste already exists',
        )

    try:
        paste_orm = await db_session.scalar(insert(Paste).values(data.dict()).returning(Paste))
        paste = PasteSchema.from_orm(paste_orm)
        await db_session.commit()
    except SQLAlchemyError as e:
        # TODO: LOGGING
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Paste cannot be created',
        )
    return paste


async def get_paste_by_hash_id(paste_hash_id: str, db_session: AsyncSession) -> PasteSchema:
    try:
        stmt = select(Paste).where(paste_hash_id == Paste.hash_id)
        paste_orm = await db_session.scalar(stmt)
        if paste_orm is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Paste not found')
        paste = PasteSchema.from_orm(paste_orm)
    except SQLAlchemyError as e:
        # TODO: LOGGING
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error',
        )
    return paste


async def get_pastes(db_session: AsyncSession) -> list[PasteSchema]:
    try:
        stmt = select(Paste)
        queryset = (await db_session.scalars(stmt)).all()
        return [PasteSchema.from_orm(paste_orm) for paste_orm in queryset]
    except SQLAlchemyError as e:
        # TODO: LOGGING
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error',
        )
