from enum import StrEnum


class RawMode(StrEnum):
    ADD = 'add'
    DELETE = 'delete'
    REMOVE = 'remove'
    RM = 'rm'

class Mode(StrEnum):
    ADD = RawMode.ADD.value.upper()
    DEL = RawMode.DELETE.value[:3].upper()
