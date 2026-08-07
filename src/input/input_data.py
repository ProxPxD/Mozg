from dataclasses import dataclass
from typing import Any

import input.concepts as concepts
from input.concepts import File, Mode


class InconsistentInputError(ValueError):
    pass


class ConflictingQuerySourcesError(InconsistentInputError):
    pass


class InlineQueryWithFileQueryError(ConflictingQuerySourcesError):
    def __init__(self, *args: Any) -> None:
        super().__init__('Inline query cannot be specified when file query is provided', *args)


class InlineQueryWithEditorQueryError(ConflictingQuerySourcesError):
    def __init__(self, *args: Any) -> None:
        super().__init__('Inline query cannot be specified when editor is requested', *args)


@dataclass
class InputData:
    mode: Mode
    file: File
    query: str

    def __post_init__(self) -> None:
        if error := self._get_validation_error():
            raise error

    def _get_validation_error(self) -> ConflictingQuerySourcesError | None:
        match bool(self.query), self.file:
            case True, concepts.file.EDITOR:
                return InlineQueryWithEditorQueryError()
            case _, concepts.file.NO_FILE:
                return None
            case True, str():
                return InlineQueryWithFileQueryError()
            case _:
                return None
