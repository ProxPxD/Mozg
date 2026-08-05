from typing import NamedTuple, Sequence

from input.consts import Ops


class Mode:
    def __init__(self, *commands: str) -> None:
        self.commands: Sequence[str] = commands

    @property
    def main(self) -> str:
        return self.commands[0]

    @property
    def substrings(self) -> list[str]:
        return list({
            command[:i+1]
            for command in self.commands
            for i in range(len(command))
        })


class Modes(NamedTuple):
    add: Mode = Mode(Ops.ADD)
    rem: Mode = Mode(Ops.REMOVE, Ops.DELETE, Ops.RM)


def detect_mode(val: str) -> str:
    matches: list[str] = [
        mode.main
        for mode in Modes()
        if val in mode.substrings
    ]

    match len(matches):
        case 1: return matches[0]
        case 0: raise ValueError(f'Unknown mode: {val}')
        case _: raise ValueError(f'Ambiguous mode: {val}: {matches}')
