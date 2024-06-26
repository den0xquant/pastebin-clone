import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from controller.paste import paste_router
from storage.db.session_manager import session_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if session_manager._engine is None:
        await session_manager.close()


pastebin = FastAPI(lifespan=lifespan)

pastebin.include_router(paste_router)


if __name__ == "__main__":
    uvicorn.run("pastebin:pastebin", host="0.0.0.0", port=6006, reload=True)
