from typing import AsyncGenerator, Any
from httpx import ASGITransport, AsyncClient
import pytest
from uuid import uuid4
from backend.app.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    host, port = (
        "127.0.0.1",
        "8000",
    )  # TODO: Weird issue? Check here, port could be 9000

    async with AsyncClient(
        transport=ASGITransport(app=app, client=(host, port)), base_url="https://test"
    ) as client:
        yield client


@pytest.fixture
def example_note():
    json = {
        "name": "Test note",
        "entry_id": str(uuid4()),
        "mode": "Note",
        "tags": ["Coding", "Practice"],
    }

    return json


@pytest.mark.entry_access
async def test_upload_entry(client: AsyncClient, example_note: dict[str, Any]):
    resp = await client.post("/entries", json=example_note)

    assert resp.status_code == 201
