import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy import (
    TIMESTAMP, UUID
)
from sqlalchemy import Table, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.schemas import Exposure, PasteCategory, Expiration


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
    }


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    last_login: Mapped[datetime] = mapped_column(server_default=func.now())
    pastes: Mapped[List["Paste"]] = relationship(back_populates="user")


association_table = Table(
    "pastes_tags",
    Base.metadata,
    Column("paste_id", ForeignKey("pastes.id")),
    Column("tag_id", ForeignKey("tags.id")),
)


class Paste(Base, TimestampMixin):
    __tablename__ = "pastes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    text: Mapped[str]
    syntax_highlight: Mapped[bool]
    exposure: Mapped[Exposure]
    category: Mapped[PasteCategory]
    expiration: Mapped[Expiration] = mapped_column(default=Expiration.NEVER)
    password_disabled: Mapped[bool] = mapped_column(default=False)
    password: Mapped[Optional[str]]
    burn_after_read: Mapped[bool] = mapped_column(default=False)
    hash_id: Mapped[Optional[str]]

    # relations
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="pastes")
    tags: Mapped[List["Tag"]] = relationship(
        secondary=association_table, back_populates="pastes")


class Tag(Base, TimestampMixin):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str]
    pastes: Mapped[List[Paste]] = relationship(
        secondary=association_table, back_populates="tags")
