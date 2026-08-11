from enum import Enum, auto


class FileState(Enum):
    NO_FILE = auto()
    NO_FLAG = auto()

type File = str | FileState
