import sys
from argparse import ArgumentParser

from input import concepts
from input.concepts import detect_mode
from input.input_data import InputData


class CLI:
    def __init__(self) -> None:
        self.parser: ArgumentParser = ArgumentParser(
            prog='Mozg',
            description='RDF GDB CLI',
            epilog='',
        )

        self.parser.add_argument('mode', type=detect_mode, help='Mode #todo')
        self.parser.add_argument('--file', '-f', nargs='?', dest='file', const=concepts.file.NO_FILE, default=concepts.file.EDITOR, help='Query File')
        self.parser.add_argument('--editor', '-e', dest='file', action='store_const', const=concepts.file.NO_FILE)

    def parse(self, args: list[str] = None) -> InputData:
        args = args or sys.argv[1:]
        args = [subarg for arg in args for subarg in arg.split('\xa0')]
        parsed, rest = self.parser.parse_known_args(args)
        return InputData(query=' '.join(rest), **vars(parsed))
