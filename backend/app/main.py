from fastapi import FastAPI
from backend.app.routers import entries

app = FastAPI()

app.include_router(entries.router)
