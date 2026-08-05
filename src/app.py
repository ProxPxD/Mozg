from input import CLI


class App:
    def __init__(self) -> None:
        self.cli = CLI()

    def run(self) -> None:
        ...

    def run_once(self) -> None:
        ...

    def run_loop(self) -> None:
        ...
