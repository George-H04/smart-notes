from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.dependencies import get_db
from backend.app.schemas import NoteEntry, NoteResponse
from ..services import build_db_entry, convert_str_to_tag

router = APIRouter()


@router.get("/entries")
def get_entries():
    # What to do here:
    #   Simply query all entries and return them... not very usefull
    return "Okay!"


@router.post(
    "/entries", status_code=status.HTTP_201_CREATED, response_model=NoteResponse
)
def upload_entry(entry: NoteEntry, session: Session = Depends(get_db)):
    # Takes in an entry model, stores in database
    tags = convert_str_to_tag(session, entry)

    db_entry = build_db_entry(entry, tags)

    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)

    return db_entry


@router.put("/entries/{id}")
def update_entry(note_id: int):
    pass


@router.delete("/entries/{id}")
def delete_entry(note_id: int):
    pass
