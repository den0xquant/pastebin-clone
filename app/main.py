from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.dependencies import session_manager
from app.routers.pastes import router as pastes_router
from app.routers.users import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if session_manager.engine is None:
        await session_manager.close()


pastebin = FastAPI(lifespan=lifespan)

pastebin.include_router(pastes_router)
pastebin.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:pastebin", host="0.0.0.0", port=6006, reload=True)
