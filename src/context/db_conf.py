import re
from collections.abc import Iterator
from dataclasses import astuple, dataclass, field
from typing import Self

uri_pattern: re.Pattern = re.compile(r'(?P<protocol>[^:]+)://(?P<host>[^:]+):(?P<port>\d{1,5})')


@dataclass(frozen=True)
class Auth:
    user: str
    password: str = field(repr=False)

    def __iter__(self) -> Iterator[str]:
        yield from astuple(self)


@dataclass(frozen=True)
class ConnectionParameters:
    protocol: str
    host: str
    port: int | str

    @property
    def uri(self) -> str:
        return f'{self.protocol}://{self.host}:{self.port}'

    @classmethod
    def from_uri(cls, uri: str) -> Self:
        if not (matched := uri_pattern.match(uri)):
            raise ValueError(f'Wrong URI format provided. Expected: {uri_pattern.pattern}, but got {uri}')
        return cls(**matched.groupdict())


@dataclass(frozen=True)
class DBConf:
    conn_params: ConnectionParameters
    auth: Auth
    repo: str

    @property
    def endpoint(self) -> str:
        return f'{self.conn_params.uri}/repositories/{self.repo}'

    @property
    def query_endpoint(self) -> str:
        return self.endpoint

    @property
    def update_endpoint(self) -> str:
        return f'{self.endpoint}/statements'
