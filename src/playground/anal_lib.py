
from typing import Any, Callable


class Analizer:
    def __init__(self,
            module: Any,
            run: Callable = None,
            format_output: Callable | str = None,
        ) -> None:
        self.module = module
        self.run = run or self.module
        self.format_output = format_output

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        result = self.run(*args, **kwds)
        match self.format_output:
            case None: output = result
            case str(): output = getattr(result, self.format_output)()
            case _ if isinstance(self.format_output, Callable): output = self.format_output(result)
        return result, output

