from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Self

from context.defaults import Defaults
from input import InputData
from input.concepts import file


@dataclass(kw_only=True)
class Context(Defaults):
    @classmethod
    def from_input_data(cls, input_data: InputData) -> Self:
        return cls(**asdict(input_data))

'''
Query Input States:
 - From File
 - From Editor
 - From Query

Keywords/Operations:
 - Add     C
 - Show    R
 - Update  U
 - Del     D
'''
