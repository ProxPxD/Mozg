from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Self

from concepts.query_source import QuerySource
from context.defaults import Defaults
from input import InputData
from input.concepts.file import FileState


@dataclass(kw_only=True)
class Context(Defaults):
    @classmethod
    def from_input_data(cls, input_data: InputData) -> Self:
        return cls(**asdict(input_data))

    @property
    def query_source(self) -> QuerySource:
        # fmt: off
        match self.file:
            case FileState.NO_FLAG: return QuerySource.COMMANDLINE
            case FileState.NO_FILE: return QuerySource.EDITOR
            case str(): return QuerySource.FILE
            case _: raise ValueError(f'Invalid state for file: {self.file}')
        # fmt: on



'''
Query Query Source:
 - From File
 - From Editor
 - From Query

Keywords/Operations:
 - Add     C
 - Show    R
 - Update  U
 - Del     D
'''
