from fastapi import FastAPI
from routers import entries

app = FastAPI()

app.include_router(entries.router)
