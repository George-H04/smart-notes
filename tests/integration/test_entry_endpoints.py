from typing import AsyncGenerator, Any
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from uuid import UUID
from sqlalchemy.orm import Session
import pytest
from uuid import uuid4
from backend.app.db.models import Note, Tag
from backend.app.enums import NoteType
from backend.app.dependencies import get_db
from asgi_lifespan import LifespanManager
from backend.app.main import app
from backend.app.services import clear_db

###############################################################
#                                                             #
#             DEFINE FIXTURES FOR TEST FUNCTIONS              #
#                                                             #
###############################################################


@pytest_asyncio.fixture(scope="session")
async def async_app():
    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture(scope="session")
async def client(async_app) -> AsyncGenerator[AsyncClient, None]:
    host, port = (
        "127.0.0.1",
        8000,
    )

    async with AsyncClient(
        transport=ASGITransport(app=async_app, client=(host, port)),
        base_url="https://test",
    ) as client:
        yield client


@pytest.fixture
def example_note():
    json = {
        "note_name": "Test note",
        "mode": NoteType.NOTE,
        "content": "This is a test note!",
        "tags": ["Coding", "Practice"],
    }

    return json


EXAMPLE_ID = uuid4()


@pytest.fixture
def example_note_db():
    return Note(
        note_name="Test note",
        note_id=EXAMPLE_ID,
        content="This is a test note!",
    )


@pytest.fixture
def updated_note():
    json = {
        "note_name": "Test note",
        "mode": NoteType.NOTE,
        "content": "This is a test note! But I forgot to add this sentence...",
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


@pytest.fixture
def tag_dict() -> dict[str, Tag]:
    tag_dict = {
        "coding": Tag(tag_name="coding"),
        "practice": Tag(tag_name="practice"),
        "piano": Tag(tag_name="piano"),
        "wood working": Tag(tag_name="wood working"),
        "diving": Tag(tag_name="diving"),
        "diet": Tag(tag_name="diet"),
        "reflection": Tag(tag_name="reflection"),
    }

    return tag_dict


CODING_ID = uuid4()
REFLECTION_ID = uuid4()
PIANO_ID = uuid4()


@pytest.fixture
def notes_list(tag_dict) -> list[Note]:
    notes = [
        Note(
            note_id=CODING_ID,
            note_name="Coding practice",
            duration_minutes=45,
            mode=NoteType.PRACTICE,
            tags=[tag_dict["coding"], tag_dict["practice"]],
            content="Today I worked on my Python API. I struggled with \
                    bulk insertion of DB elements, but eventually I \
                    figured it out. Now I am writing test cases so I can \
                    efficiently continue development.",
        ),
        Note(
            note_id=REFLECTION_ID,
            note_name="Daily Reflection",
            mode=NoteType.JOURNAL,
            tags=[tag_dict["reflection"]],
            content="Today has been a good day. Although I am still sick, \
                    I am definitely feeling better. Mentally, I am alright. \
                    Could always be better, but for now, I am living life.",
        ),
        Note(
            note_id=PIANO_ID,
            note_name="Piano practice",
            duration_minutes=60,
            mode=NoteType.PRACTICE,
            tags=[tag_dict["piano"], tag_dict["practice"]],
            content="Piano practice went well today, I managed to play my \
                    assigned scales very cleany, and with proper posture. \
                    I am sure my piano teacher will be proud of my development. \
                    However, I still have trouble with my arpeggios. There is \
                    stiffness and delay whenever I have to cross my fingers.",
        ),
    ]

    return notes


###############################################################
#                                                             #
#                       START TEST CASES                      #
#                                                             #
###############################################################


@pytest.mark.anyio
async def test_upload_entry(
    client: AsyncClient, example_note: dict[str, Any], db_instance: Session
):
    clear_db(db_instance)

    resp = await client.post("/entries", json=example_note)

    assert resp.status_code == 201


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input,expected",
    [
        ({"tags": "coding"}, {CODING_ID}),
        ({"tags": "practice"}, {CODING_ID, PIANO_ID}),
        ({"tags": "reflection"}, {REFLECTION_ID}),
        ([("tags", "coding"), ("tags", "reflection")], {CODING_ID, REFLECTION_ID}),
        ([], {CODING_ID, PIANO_ID, REFLECTION_ID}),
    ],
)
async def test_get_entries(
    input, expected, client: AsyncClient, notes_list: list[Note], db_instance: Session
):
    clear_db(db_instance)

    # Seed DB with test data
    db_instance.add_all(notes_list)
    db_instance.commit()

    if input:
        resp = await client.get("/entries", params=input)
    else:
        resp = await client.get("/entries")

    assert resp.status_code == 200

    retrieved_notes = {UUID(note["note_id"]) for note in resp.json()}

    assert expected == retrieved_notes


@pytest.mark.asyncio
async def test_update_entry(
    client: AsyncClient, db_instance: Session, example_note_db, updated_note
):
    pass
    clear_db(db_instance)

    # Seed db with an example note object
    db_instance.add(example_note_db)

    resp = await client.put("/entries", json=updated_note)

    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_delete_entry(note_id: UUID, client: AsyncClient, db_instance: Session):
    pass
    clear_db(db_instance)

    db_instance.add(example_note_db)

    resp = await client.delete("/entries/{note_id}")

    assert resp.status_code == 200
