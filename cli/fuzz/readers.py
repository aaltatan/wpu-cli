from collections.abc import Callable
from functools import wraps
from pathlib import Path

from cli.utils import extract_extension

type ReaderFn = Callable[[Path], list[str]]


_readers: dict[str, ReaderFn] = {}


def get_readers() -> dict[str, ReaderFn]:
    return _readers.copy()


def get_reader_data(path: Path) -> list[str]:
    extension = extract_extension(path)
    return _readers[extension](path)


def register_reader(reader: str) -> Callable[[ReaderFn], ReaderFn]:
    def decorator(reader_fn: ReaderFn) -> ReaderFn:
        @wraps(reader_fn)
        def wrapper(path: Path) -> list[str]:
            return reader_fn(path)

        _readers[reader] = wrapper
        return wrapper

    return decorator


@register_reader("txt")
def get_data_from_txt_file(path: Path) -> list[str]:
    with open(path, encoding="utf-8") as file:  # noqa: PTH123
        return file.read().splitlines()
