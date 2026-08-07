from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Self

from context.defaults import Defaults
from input import InputData


@dataclass(kw_only=True)
class Context(Defaults):
    @classmethod
    def from_input_data(cls, input_data: InputData) -> Self:
        return cls(**asdict(input_data))
