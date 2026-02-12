from fastapi import APIRouter, status
from backend.app.models import Entry

router = APIRouter()


@router.get("/entries")
def get_entries():
    # What to do here:
    #   Simply query all entries and return them... not very usefull
    return "Okay!"


@router.post("/entries", status_code=status.HTTP_201_CREATED)
def upload_entry(entry: Entry):
    # Takes in an entry model, stores in database
    return "201"


@router.put("/entries/{id}")
def update_entry(note_id: int):
    pass


@router.delete("/entries/{id}")
def delete_entry(note_id: int):
    pass
