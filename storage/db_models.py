from uuid import uuid4
from sqlalchemy import (Column, DateTime, Integer, String, Text, UUID)
from sqlalchemy.sql import func

from . import Base


class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)


class Paste(Base, TimestampMixin):
    __tablename__ = 'pastes'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
