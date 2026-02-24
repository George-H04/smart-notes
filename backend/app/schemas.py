"""
Schemas to use across the application for Pydantic data validation
"""

import uuid
from datetime import datetime
from typing import Annotated

from .enums import NoteType
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from backend.app.db.models import Tag


def _normalize_tags(tag_list: list[str]) -> list[str] | None:
    return list(set(tag.lower().strip() for tag in tag_list)) if tag_list else None


def _convert_tags_to_str(tag_list: list[Tag]) -> list[str]:
    return [tag.tag_name for tag in tag_list]


class NoteBase(BaseModel):
    note_name: str = Field(max_length=100)
    duration_minutes: int | None = None
    mode: NoteType = NoteType.NOTE
    content: str


class NoteEntry(NoteBase):
    tags: Annotated[list[str] | None, BeforeValidator(_normalize_tags)] = None


class NoteResponse(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    note_id: uuid.UUID
    tags: Annotated[list[str] | None, BeforeValidator(_convert_tags_to_str)] = None
    created_at: datetime
