# from editor import editor
import sys

from app import App
from input.input_data import InconsistentInputError

# text = editor()

# print(text)

if __name__ == '__main__':
    try:
        App().run()
    except InconsistentInputError as error:
        print(error, file=sys.stderr)  # noqa: T201
        sys.exit(1)
