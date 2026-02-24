from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.routers import entries
from .db.engine import engine
from .db.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(entries.router)
