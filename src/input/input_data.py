from dataclasses import dataclass

from input.consts import Ops


@dataclass
class InputData:
    mode: Ops
    rest: str
