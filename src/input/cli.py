import sys
from argparse import ArgumentParser

from concepts.sentinels import NO_ARG, UNUSED

from .concepts import detect_mode
from .input_data import InputData


class CLI:
    def __init__(self) -> None:
        self.parser: ArgumentParser = ArgumentParser(
            prog='Mozg',
            description='RDF GDB CLI',
            epilog='',
        )

        self.parser.add_argument('mode', type=detect_mode, help='Mode #todo')
        self.parser.add_argument('--file', '-f', nargs='?', dest='file', const=NO_ARG, default=UNUSED, help='Query File')
        self.parser.add_argument('--editor', '-e', dest='file', action='store_const', const=NO_ARG)

    def parse(self, args: list[str] = None) -> InputData:
        args = args or sys.argv[1:]
        args = [subarg for arg in args for subarg in arg.split('\xa0')]
        parsed, rest = self.parser.parse_known_args(args)
        return InputData(query=' '.join(rest), **vars(parsed))
