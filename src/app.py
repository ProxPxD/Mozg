from context import Context
from input import CLI, InputData


class App:
    def __init__(self) -> None:
        self.cli = CLI()
        self.cxt: Context = Context()

    def run(self) -> None:
        input_data: InputData = self.cli.parse()
        self.cxt = Context.from_input_data(input_data)
        match self.cxt.loop:
            case True: self.run_loop()
            case False: self.run_once()

    def run_loop(self) -> None:
        while self.cxt.loop:
            self.run_once()

    def run_once(self) -> None:
        ...
