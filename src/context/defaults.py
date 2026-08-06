
from dataclasses import dataclass

from input.consts import Mode


@dataclass
class Defaults:
    loop: bool = False
    mode: Mode | None = None
    query: str | None = None
