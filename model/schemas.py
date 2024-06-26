import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from model.base import TimeMixin
from model.utils import PasteCategory, Exposure


class UserSchema(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    password: str
    is_active: bool
    last_login: datetime
    pastes: list["PasteSchema"]


class TagSchema(BaseModel, TimeMixin):
    id: int
    name: str
    pastes: list["PasteSchema"]


class PasteSchema(BaseModel, TimeMixin):
    id: int
    name: str
    text: str
    syntax_highlight: bool
    exposure: Exposure
    category: PasteCategory

    password_disabled: bool
    password: Optional[str]
    expiration: datetime
    burn_after_read: bool

    hash_id: str

    # relations
    user_id: uuid.UUID
    user: UserSchema
    tags: list[TagSchema]
