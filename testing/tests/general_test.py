from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from core.tcg import TCG

type StrS = str | Sequence[str]


@dataclass
class TC:
    descr: str

    setup: StrS
    check: StrS
    file: StrS
    expect: StrS

    tags: set[str] = field(default_factory=set)


class ExemplaryTCG(TCG):
    tcs = [
        
    ]


@ExemplaryTCG.parametrize('tc')
def test(tc: TC) -> None:
    ...
