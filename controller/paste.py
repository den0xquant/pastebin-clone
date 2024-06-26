import http

from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from storage.db.models import Paste
from storage.db.session_manager import get_db_session


paste_router = APIRouter(prefix="/v1/pastes", tags=["paste_router", "paste"])


# @paste_router.post("/create", status_code=http.HTTPStatus.OK)
# async def create_block(create_model: create.CreateBlock):
#     return response


@paste_router.get("/{paste_id}", status_code=http.HTTPStatus.OK)
async def get_paste(paste_id: int, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    response = (await db_session.scalars(select(Paste).where(paste_id == Paste.id))).first()
    return response


# @paste_router.put("/update/{paste_id}", status_code=http.HTTPStatus.OK)
# async def update_paste(update_paste: update.UpdatePaste):
#     ...
#
#
# @paste_router.delete("/delete", status_code=http.HTTPStatus.OK)
# async def delete_block(_=Depends(build_request_context)):
#     """
#     Delete API key
#     :param _: build_request_context dependency injection handles the request context
#     :param api_key: API key to delete
#     :return:
#     """
#     response: GenericResponseModel = AdminUseCase.delete_api_keys(api_key=api_key)
#     return build_api_response(response)
