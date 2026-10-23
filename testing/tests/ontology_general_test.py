from __future__ import annotations
from SPARQLWrapper import SPARQLWrapper
import pytest

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from core.tcg import TCG

type StrS = str | Sequence[str]

@dataclass
class TC:
    descr: str
    init_query: str
    checks: list[Check]


@dataclass
class Check:
    descr: str
    query: str
    expected: Any


class OntologyTCG(TCG):
    tcs = [
        TC(
            descr='',
            init_query='',
            checks=[
                Check(
                    descr='',
                    query='',
                    expected='',
                ),
            ],
        ),
    ]


@pytest.fixture
def sparql() -> SPARQLWrapper:
    endpoint = "http://localhost:7001/repositories/test-repo"
    return SPARQLWrapper(
        query_endpoint,
        updateEndpoint=update_endpoint,
    )


@OntologyTCG.parametrize('tc')
def test(tc: TC) -> None:
    ...
