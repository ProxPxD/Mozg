from enum import StrEnum
from typing import NamedTuple

import input.concepts.keywords.mode as raw_mode


class Mode(StrEnum):
    ADD = raw_mode.ADD.upper()
    DEL = raw_mode.DELETE[:3].upper()


class ComlexMode:
    def __init__(self, *commands: str, repr_: str = None) -> None:
        self.repr: str = repr_ or self.commands[0]
        self.commands: list[str] = list(commands)

    def is_substring(self, value: str) -> bool:
        return any(command.startswith(value) for command in self.commands)

    @property
    def substrings(self) -> list[str]:
        return list({
            command[:i+1]
            for command in self.commands
            for i in range(len(command))
        })


    def __contains__(self, value: str) -> bool:
        return self.is_substring(value)


class ComplexModes(NamedTuple):
    add: ComlexMode = ComlexMode(raw_mode.ADD, repr_=Mode.ADD)
    rem: ComlexMode = ComlexMode(raw_mode.REMOVE, raw_mode.DELETE, raw_mode.RM, repr_=Mode.DEL)


def detect_mode(val: str) -> str:
    matches: list[str] = [
        mode.repr
        for mode in ComplexModes()
        if val in mode
    ]

    match len(matches):
        case 1: return matches[0]
        case 0: raise ValueError(f'Unknown mode: {val}')
        case _: raise ValueError(f'Ambiguous mode: {val}: {matches}')
