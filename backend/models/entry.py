import datetime
from pydantic import BaseModel

class Entry(BaseModel):
    name: str                       # Name of the entry
    entry_id: int                         # Generated ID of the entry
    duration: int | None = None     # Optional: Duration if a session of something
    timestamp: datetime             # Timestamp of the entry 
    mode: str | None = None         # Optional: Note | Sessions | reflection
    tags: list[str] | None = None   # Optional: List of tags categorizing the entry
    