from enum import Enum


class ResourceType(Enum):
    PROJECTS = "projects"
    ALL = "all"
    ITEMS = "items"
    LABELS = "labels"
    NOTES = "notes"
    STATS = "stats"
