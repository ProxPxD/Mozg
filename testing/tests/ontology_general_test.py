from __future__ import annotations

import pydash as _
from pydash import chain as c
import os
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from textwrap import dedent
from typing import Any

import pytest
from core.tcg import TCG
from SPARQLWrapper import GET, JSON, POST, SPARQLWrapper

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
                    :Clause :feat :Subject.
                    :Action
                        :sub :Clause;
                        :feat :Actor, :Undergoer.
                    :Source
                        :sub :Action;
                        :feat :SourceRole, :SourceOfRole.
                    :SourceRole :sub :Subject.
                    :SourceOfRole :sub :Subject.
                    :Watch
                        :sub :Action;
                        :feat :WatcherRole, :WatchedRole.
                    :WatcherRole :sub :Actor.
                    :WatchedRole :sub :Undergoer.
                    :Want
                        :sub :Action;
                        :feat :WanterRole, :WantedRole.
                    :WanterRole :sub :Actor.       # Experiencer?
                    :WantedRole :sub :Undergoer.   # Stimulus?
                    :Should
                        :sub :Action;
                        :feat :ObligedRole, :DutyRole.
                    :ObligedRole :sub :Actor.
                    :DutyRole :sub :Undergoer.

                    :pl-dane-link
                        :val "https://www.youtube.com/watch?v=E89x6LpA6Uw";
                        :is :link;
                        :feat :youtube .
                    :swiss-political-system
                        :name "Swiss Political System"

                    :source-inst-1
                        :feat :source-role-1, :source-of-role-1;
                        :is :Source .
                    :source-role-1
                        :is :SourceRole;
                        :feat :pl-dane-link .
                    :source-of-role-1
                        :is :SourceOfRole;
                        :feat :swiss-political-system.

                    :want-inst-1
                        :feat :wanter-role-1, :wanted-role-1;
                        :is :Want .
                    :wanter-role-1
                        :is :WanterRole;
                        :feat :piotr .
                    :wanted-role-1
                        :is :WantedRole;
                        :feat :watch-inst-1.

                    :watch-inst-1
                        :feat :watcher-role-1, :watched-role-1;
                        :is :Watch .
                    :watcher-role-1
                        :is :WatcherRole;
                        :feat :anhi .
                    :watched-role-1
                        :is :WatchedRole;
                        :feat :pl-dane-link.

                    :should-inst-1
                        :feat :shoulder-role-1, :shoulded-role-1;
                        :is :Should .
                    :shoulder-role-1
                        :is :ObligedRole;
                        :feat :anhi .
                    :shoulded-role-1
                        :is :DutyRole;
                        :feat :watch-inst-1.  # ?Maybe watcher-role-1
                }
            '''),
            checks=[
                Check(
                    descr='',
                    query='''
                        PREFIX : <mozg:test:>
                        SELECT *
                        WHERE {
                            ?topic
                                :name "Swiss Political System";
                                ^:feat+ ?relation.
                            ?relation
                                :is/:sub+ :Clause ;
                                :feat ?argument.
                            ?argument
                                :is/:sub :Subject;
                                :feat+ ?node .
                            ?node ?prop ?val .
                        }
                    ''',
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
    sparql.setReturnFormat(JSON)


@pytest.fixture(scope='module', autouse=False)  # TODO: set to autose
def teardown_session(sparql):
    yield
    sparql.setMethod(POST)
    sparql.setQuery('CLEAR DEFAULT')
    sparql.query()


@OntologyTCG.parametrize('tc')
def test(tc: Tc, sparql: SPARQLWrapper, meta: Meta) -> None:
    sparql.setQuery(tc.check_query)
    result = sparql.query().convert()
    bindings, headers = _.at(result, 'results.bindings', 'head.vars')  # pyright: ignore[reportCallIssue]
    print()
    print('\t'.join(headers))
    for binding in bindings:
        keys = binding.keys()
        vals = c(binding).at(*keys).map(c().get('value').replace_start('mozg:test:', '')).value()
        print('\t'.join(vals))
    pytest.exit(NotImplemented)
