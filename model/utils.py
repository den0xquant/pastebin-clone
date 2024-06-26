from enum import Enum


class Exposure(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"


class PasteCategory(Enum):
    PROGRAMMING = "Programming"
    CONFIGURATION_FILES = "Configuration Files"
    SCRIPTS = "Scripts"
    DOCUMENTATION = "Documentation"
    LOGS = "Logs"
    DATA = "Data"
    SNIPPETS = "Snippets"
    NOTES = "Notes"
    TEXT = "Text"
    TEMPLATES = "Templates"
    SECURITY = "Security"
    MISCELLANEOUS = "Miscellaneous"
