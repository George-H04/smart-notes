from fastapi import APIRouter

router = APIRouter()

@router.get("/entries")
def get_entries():
    # What to do here:
    #   Simply query all entries and return them... not very useful
    return "Okay!"

@router.post("/entries")
def upload_entry(entry: str):
    # Takes in an entry
    pass

@router.put("/entries/{id}")
def update_entry(note_id: int):
    pass

@router.delete("/entries/{id}")
def delete_entry(note_id: int):
    pass