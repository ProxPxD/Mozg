from enum import StrEnum


class Ops(StrEnum):
    ADD = 'add'
    DELETE = 'delete'
    REMOVE = 'remove'
    RM = 'rm'

class Mode(StrEnum):
    ADD = Ops.ADD.value.upper()
    DEL = Ops.DELETE.value[:3].upper()
