from input import CLI, InputData


class App:
    def __init__(self) -> None:
        self.cli = CLI()

    def run(self) -> None:
        input_data: InputData = self.cli.parse()

    def run_once(self) -> None:
        ...

    def run_loop(self) -> None:
        ...
