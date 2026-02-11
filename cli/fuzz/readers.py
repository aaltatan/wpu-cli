from collections.abc import Callable
from functools import wraps
from pathlib import Path

from cli.utils import extract_extension

type ReaderFn = Callable[[Path], list[str]]


class ReaderRegistry:
    def __init__(self) -> None:
        self._readers: dict[str, ReaderFn] = {}

    def __contains__(self, reader: str) -> bool:
        return reader in self._readers

    def __getitem__(self, reader: str) -> ReaderFn:
        if reader not in self._readers:
            message = f"Reader '{reader}' not found"
            raise ValueError(message)

        return self._readers[reader]

    def get_reader_data(self, path: Path) -> list[str]:
        extension = extract_extension(path)
        return self[extension](path)

    def register(self, reader: str) -> Callable[[ReaderFn], ReaderFn]:
        def decorator(reader_fn: ReaderFn) -> ReaderFn:
            @wraps(reader_fn)
            def wrapper(path: Path) -> list[str]:
                return reader_fn(path)

            self._readers[reader] = wrapper
            return wrapper

        return decorator


readers = ReaderRegistry()


@readers.register("txt")
def get_data_from_txt_file(path: Path) -> list[str]:
    with open(path, encoding="utf-8") as file:  # noqa: PTH123
        return file.read().splitlines()
