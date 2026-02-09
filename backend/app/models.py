import datetime
from pydantic import BaseModel
from uuid import uuid4
from sqlmodel import Field


class Entry(BaseModel):
    name: str                      
    entry_id: int = Field(unique=True, default_factory=uuid4)              
    duration: int | None = None     
    timestamp: datetime              
    mode: str | None = None         
    tags: list[str] | None = None
