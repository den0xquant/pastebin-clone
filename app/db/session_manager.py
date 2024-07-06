import contextlib
from typing import AsyncIterator, Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    AsyncConnection,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine: AsyncEngine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker: async_sessionmaker = async_sessionmaker(bind=self._engine)

    @property
    def engine(self):
        return self._engine

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception:
                await conn.rollback()
                raise


session_manager = DatabaseSessionManager(host=settings.database_url, engine_kwargs={"echo": True})
