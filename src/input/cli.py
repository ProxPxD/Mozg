import sys
from argparse import ArgumentParser

from input.concepts import detect_operation
from input.concepts.file import FileState
from input.input_data import InputData


class CLI:
    def __init__(self) -> None:
        self.parser: ArgumentParser = ArgumentParser(
            prog='Mozg',
            description='RDF GDB CLI',
            epilog='',
        )

        self.parser.add_argument('operation', type=detect_operation, help='Operation #todo')
        self.parser.add_argument('--file', '-f', nargs='?', dest='file', const=FileState.NO_FILE, default=FileState.NO_FLAG, help='Query File')
        self.parser.add_argument('--editor', '-e', dest='file', action='store_const', const=FileState.NO_FILE, help='Open editor to query')

    def parse(self, args: list[str] = None) -> InputData:
        args = args or sys.argv[1:]
        args = [subarg for arg in args for subarg in arg.split('\xa0')]
        parsed, rest = self.parser.parse_known_args(args)
        return InputData(input=' '.join(rest), **vars(parsed))
