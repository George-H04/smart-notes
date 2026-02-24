from enum import Enum


class NoteType(str, Enum):
    NOTE = "note"
    PRACTICE = "practice"
    HEALTH = "health"
    NUTRITION = "nutrition"
    JOURNAL = "journal"
    GOAL = "goal"
