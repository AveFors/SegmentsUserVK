from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager


from core.models.db_helper import db_helper
from core.models.base import Base

from api_v1 import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix='/api')


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


