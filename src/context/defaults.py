
from dataclasses import dataclass

from input import Mode


@dataclass
class Defaults:
    loop: bool = False
    mode: Mode | None = None
    query: str | None = None
    file: str | None = None
