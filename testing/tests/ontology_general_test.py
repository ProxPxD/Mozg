from __future__ import annotations

import os
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from textwrap import dedent
from typing import Any

import pytest
from core.tcg import TCG
from SPARQLWrapper import GET, POST, SPARQLWrapper

from context.db_conf import Auth, ConnectionParameters, DBConf

type StrS = str | Sequence[str]

@dataclass
class Meta:
    last_init_query: str = ''


@pytest.fixture(scope='module')
def meta() -> Meta:
    return Meta()


@pytest.fixture(scope='module')
def db_conf() -> DBConf:
    return DBConf(
        auth=Auth(
            user=os.environ['TEST_DB_USER'],
            password=os.environ['TEST_DB_PASSWORD'],
        ),
        conn_params=ConnectionParameters.from_uri('http://localhost:7020'),
        repo='mozg-test',
    )


@pytest.fixture(scope='module')
def sparql(db_conf: DBConf) -> SPARQLWrapper:
    return SPARQLWrapper(
        db_conf.query_endpoint,
        updateEndpoint=db_conf.update_endpoint,
    )


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

@dataclass
class Tc:
    descr: str
    init_query: str
    check_query: str
    expected: Any


class OntologyTCG(TCG):
    tcs = [
        # TODO: add a duty for someone else by "want" to watch a source of ...
        # "Swiss Political System" that should have appriopritate context tags
        TC(
            descr='',
            init_query=dedent('''
                PREFIX : <mozg:test:>

                INSERT DATA {
                    :pl-dane-link
                        :val "https://www.youtube.com/watch?v=E89x6LpA6Uw";
                        :is :link;
                        :feat :youtube .
                    :switss-political-system
                        :name "Swiss Political System"

                    :Source :feat :SourceRole, :SourceOfRole.

                    :source-inst
                        :feat :source-role-1, :source-of-role-1;
                        :is :Source .
                    :source-role-1
                        :is :SourceRole;
                        :feat :pl-dane-link .
                    :source-of-role-1
                        :is :SourceOfRole;
                        :feat :switss-political-system.
                }
            '''),
            checks=[
                Check(
                    descr='',
                    query='',
                    expected='',
                ),
            ],
        ),
    ]

    @classmethod
    def map_to_many(cls, tc: TC) -> Iterable[Tc]:
        for check in tc.checks:
            yield Tc(
                descr=f'{tc.descr} - {check.descr}',
                init_query=tc.init_query,
                check_query=check.query,
                expected=check.expected,
            )


@pytest.fixture(autouse=True)
def setup_case(tc: Tc, sparql: SPARQLWrapper, meta: Meta) -> None:
    if tc.init_query != meta.last_init_query:
        sparql.setMethod(POST)
        sparql.setQuery('CLEAR DEFAULT')
        sparql.query()
        sparql.setQuery(tc.init_query)
        sparql.query()
        meta.last_init_query = tc.init_query
    sparql.setMethod(GET)


@pytest.fixture(scope='module', autouse=False)  # TODO: set to autose
def teardown_session(sparql):
    yield
    sparql.setMethod(POST)
    sparql.setQuery('CLEAR DEFAULT')
    sparql.query()


@OntologyTCG.parametrize('tc')
def test(tc: Tc, sparql: SPARQLWrapper, meta: Meta) -> None:
    ...
