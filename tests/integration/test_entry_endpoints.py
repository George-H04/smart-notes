from typing import AsyncGenerator, Any
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from sqlalchemy.orm import Session
import pytest
from uuid import uuid4
from backend.app.enums import NoteType
from backend.app.dependencies import get_db
from asgi_lifespan import LifespanManager
from backend.app.main import app


@pytest_asyncio.fixture
async def async_app():
    async with LifespanManager(app) as manager:
        print("Database tables created!")
        yield manager.app


@pytest_asyncio.fixture
async def client(async_app) -> AsyncGenerator[AsyncClient, None]:
    host, port = (
        "127.0.0.1",
        8000,
    )  # TODO: Weird issue? Check here, port could be 9000

    async with AsyncClient(
        transport=ASGITransport(app=async_app, client=(host, port)),
        base_url="https://test",
    ) as client:
        yield client


@pytest.fixture
def example_note():
    json = {
        "note_name": "Test note",
        "entry_id": str(uuid4()),
        "mode": NoteType.NOTE,
        "content": "This is a test note!",
        "tags": ["Coding", "Practice"],
    }

    return json


@pytest.fixture
def db_instance():
    session_gen = get_db()
    session = next(session_gen)

    try:
        yield session
    finally:
        try:
            next(session_gen)
        except StopIteration:
            pass


@pytest.mark.anyio
async def test_upload_entry(
    client: AsyncClient, example_note: dict[str, Any], db_instance: Session
):
    resp = await client.post("/entries", json=example_note)

    assert resp.status_code == 201
