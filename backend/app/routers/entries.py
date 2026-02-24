from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import update
from sqlalchemy.orm import Session

from backend.app.db.models import Note
from backend.app.dependencies import get_db
from backend.app.schemas import NoteEntry, NoteResponse
from ..services import build_db_entry, convert_str_to_tag, get_notes_from_tags

router = APIRouter()


@router.get("/entries", response_model=list[NoteResponse])
def get_entries(
    tags: list[str] = Query(default=[]), session: Session = Depends(get_db)
):
    """Endpoint that retrieves a set of notes that are tagged with the given parameter

    Returns:
        notes List[NoteResponse]: All notes with the queried tags
    """
    if tags == []:
        return session.query(Note).all()

    return get_notes_from_tags(session, tags)


@router.post(
    "/entries", status_code=status.HTTP_201_CREATED, response_model=NoteResponse
)
def upload_entry(entry: NoteEntry, session: Session = Depends(get_db)):
    """Endpoint for uploading notes

    Args:
        entry (NoteEntry): The note to upload
        session (Session, optional): A session from the database pool. Defaults to Depends(get_db).

    Returns:
        entry NoteResponse: The note that was uploaded
    """
    tags = convert_str_to_tag(session, entry)

    db_entry = build_db_entry(entry, tags)

    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)

    return db_entry


@router.put("/entries/{note_id}", response_model=NoteResponse)
def update_entry(entry: NoteEntry, note_id: int, db_instance: Session):
    db_instance.execute(update(Note).where())


@router.delete("/entries/{id}")
def delete_entry(note_id: int):
    pass
