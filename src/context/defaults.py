from dataclasses import dataclass

from input import Operation


@dataclass
class Defaults:
    loop: bool = False
    operation: Operation | None = None
    input: str | None = None
    file: str | None = None
