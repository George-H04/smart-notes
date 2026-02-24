"""
The SQLAlchemy models to use for ORM.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from ..enums import NoteType
from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, String, Table, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# Purely relational table, allows querying all notes that contain a given tag / given tags
note_tags = Table(
    "note_tag",
    Base.metadata,
    Column("note_id", ForeignKey("notes_table.note_id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.tag_id"), primary_key=True),
)


class Note(Base):
    __tablename__ = "notes_table"

    note_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    note_name: Mapped[str] = mapped_column(String(100))
    duration_minutes: Mapped[Optional[int]]
    mode: Mapped[NoteType] = mapped_column(SAEnum(NoteType), default=NoteType.NOTE)
    tags: Mapped[List["Tag"]] = relationship(
        secondary=note_tags, back_populates="notes"
    )
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Tag(Base):
    __tablename__ = "tags"

    tag_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    tag_name: Mapped[str] = mapped_column(String(50), unique=True)
    notes: Mapped[List["Note"]] = relationship(
        secondary=note_tags, back_populates="tags"
    )
