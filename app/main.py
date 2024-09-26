import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.config import settings
from core.db import db_helper

from api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan,
    title="ApiTaskManager",
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
