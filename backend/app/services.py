"""
Helper methods and functions for performing heavy logic.
"""

from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models import Note, Tag
from backend.app.schemas import NoteEntry


def _add_tag(session: Session, tag: str) -> Tag:
    """
    Private helper function that adds new tags to the database

    :param session: The current database session
    :type session: Session
    :param tag: The name of the tag to create
    :type tag: str
    :return: Returns the new Tag object
    :rtype: Tag
    """

    new_tag = Tag(tag_name=tag)

    session.add(new_tag)

    return new_tag


def convert_str_to_tag(session: Session, entry: NoteEntry) -> List[Tag] | None:
    """
    Converts a list of strings into a list of Tag objects

    :param session: The current database sesssion
    :type session: Session
    :param tag_list: The list of tags as strings
    :type tag_list: List[str]
    :return: The list of tags as Tag objects
    :rtype: List[Tag]
    """
    tag_list = entry.tags

    if not tag_list:
        return None

    resolved_tags: List[Tag] = []

    existing_tags = (
        session.execute(select(Tag).where(Tag.tag_name.in_(tag_list))).scalars().all()
    )
    resolved_tags += existing_tags

    if len(resolved_tags) == len(tag_list):
        return resolved_tags

    existing_tag_names = [tag.tag_name for tag in existing_tags]

    tags_to_add = set(tag_list) - set(existing_tag_names)

    for tag in tags_to_add:
        resolved_tags.append(_add_tag(session, tag.lower()))

    return resolved_tags


def build_db_entry(entry, tags):
    db_entry = Note(
        note_name=entry.note_name,
        duration_minutes=entry.duration_minutes,
        mode=entry.mode,
        tags=tags,
        content=entry.content,
    )

    return db_entry
