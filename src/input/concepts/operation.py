from enum import StrEnum
from typing import NamedTuple

import input.concepts.keywords.operation as raw_op


class Operation(StrEnum):
    ADD = raw_op.ADD.upper()
    DEL = raw_op.DELETE[:3].upper()


class ComlexOperation:
    def __init__(self, *commands: str, repr_: str = None) -> None:
        self.commands: list[str] = list(commands)
        self.repr: str = repr_ or self.commands[0]

    def is_substring(self, value: str) -> bool:
        return any(command.startswith(value) for command in self.commands)

    @property
    def substrings(self) -> frozenset[str]:
        return frozenset(command[: i + 1] for command in self.commands for i in range(len(command)))

    def __contains__(self, value: str) -> bool:
        return self.is_substring(value)


class ComplexOperaions(NamedTuple):
    add: ComlexOperation = ComlexOperation(raw_op.ADD, repr_=Operation.ADD)
    del_: ComlexOperation = ComlexOperation(raw_op.DELETE, raw_op.REMOVE, raw_op.RM, repr_=Operation.DEL)


def detect_operation(val: str) -> str:
    matches: list[str] = [op.repr for op in ComplexOperaions() if val in op]

    match len(matches):
        case 1: return matches[0]
        case 0: raise ValueError(f'Unknown mode: {val}')
        case _: raise ValueError(f'Ambiguous mode: {val}: {matches}')
