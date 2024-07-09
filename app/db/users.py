from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orm import User
from app.models.schemas import UserSchema


async def get_user_by_username(username: str, db_session: AsyncSession) -> UserSchema:
    try:
        stmt = select(User).where(username == User.username)
        user_orm = (await db_session.scalars(stmt)).first()
        if user_orm is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user = UserSchema.from_orm(user_orm)
    except SQLAlchemyError as e:
        # TODO: LOGGING
        print(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error',
        )
    return user
