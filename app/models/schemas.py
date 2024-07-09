import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class Exposure(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"


class PasteCategory(Enum):
    PROGRAMMING = "Programming"
    CONFIGURATION_FILES = "Configuration Files"
    SCRIPTS = "Scripts"
    DOCUMENTATION = "Documentation"
    LOGS = "Logs"
    DATA = "Data"
    SNIPPETS = "Snippets"
    NOTES = "Notes"
    TEXT = "Text"
    TEMPLATES = "Templates"
    SECURITY = "Security"
    MISCELLANEOUS = "Miscellaneous"


ExpirationMapping: dict[str, timedelta] = {
    "NEVER": timedelta(0),
    "MINUTES_10": timedelta(seconds=10),
    "HOUR": timedelta(hours=1),
    "DAY": timedelta(days=1),
    "WEEK": timedelta(weeks=1),
    "MONTH": timedelta(days=30),
    "YEAR": timedelta(days=365),
}


class Expiration(Enum):
    NEVER = 'never'
    MINUTES_10 = 'minutes_10'
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'


class APIError(BaseModel):
    code: int | str
    message: str


class APIResponse(BaseModel):
    success: bool
    response: dict[str, Any] | list
    status_code: int
    error: APIError | None = None


class TimeMixin(BaseModel):
    created_at: datetime
    updated_at: datetime | None


class CreateUserSchema(BaseModel):
    username: str
    email: str
    hashed_password: str


class UserSchema(CreateUserSchema):
    id: uuid.UUID
    is_active: bool
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


class TagSchema(TimeMixin):
    id: int
    name: str
    pastes: list["PasteSchema"]


class CreatePasteSchema(BaseModel):
    hash_id: Optional[str]
    name: str
    text: str
    syntax_highlight: bool
    exposure: Exposure
    category: PasteCategory
    password_disabled: bool
    password: Optional[str]
    burn_after_read: bool
    expiration: Expiration

    class Config:
        from_attributes = True

    def set_hash_id(self, hash_id: str):
        self.hash_id = hash_id


class PasteSchema(CreatePasteSchema, TimeMixin):
    id: int
    hash_id: str
    expiration: Expiration


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
