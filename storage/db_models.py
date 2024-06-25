from uuid import uuid4
from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, Text, UUID
)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    last_login = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean(), default=True)


class Paste(Base, TimestampMixin):
    __tablename__ = 'pastes'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    syntax_highlight = Column(Text, nullable=False)
    exposure = Column(DateTime, nullable=False)
    expiration = Column(DateTime, nullable=False)
    password_disabled = Column(Boolean(), default=False)
    password = Column(String, nullable=True)
    burn_after_read = Column(Boolean(), default=False)

    # relations
    user = Column(...)
    category = Column(nullable=True)
    tags = Column(...)


class Category(Base, TimestampMixin):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False)


class Tag(Base, TimestampMixin):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False)

