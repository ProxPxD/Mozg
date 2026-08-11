from enum import Enum, auto


class QuerySource(Enum):
    FILE = auto()
    EDITOR = auto()
    COMMANDLINE = auto()
