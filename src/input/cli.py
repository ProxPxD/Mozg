import sys
from argparse import ArgumentParser

from modes import detect_mode

from input.input_data import InputData


class CLI:
    def __init__(self) -> None:
        self.parser: ArgumentParser = ArgumentParser(
            prog='Mozg',
            description='RDF GDB CLI',
            epilog='',
        )

        self.parser.add_argument('mode', type=detect_mode, help='Mode #todo')
        self.parser.add_argument('query', nargs='*', help='Query #todo')

    def parse(self, args: list[str] = None) -> InputData:
        all_args = args or sys.argv[1:]
        main_args, rest_args = all_args[0:1], all_args[1:]
        parsed = self.parser.parse_args(main_args)
        parsed.rest = ' '.join(rest_args)
        return InputData(**vars(parsed))
