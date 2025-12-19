from collections.abc import Callable
from functools import wraps
from pathlib import Path

from cli.clipboard import get_clipboard
from cli.utils import extract_extension

type LoaderFn = Callable[[Path], list[str]]


_loaders: dict[str, LoaderFn] = {}


def get_loaders() -> dict[str, LoaderFn]:
    return _loaders.copy()


def get_clipboard_data() -> list[str]:
    clipboard = get_clipboard()
    return [line for line in clipboard.splitlines() if line]


def get_loader_data(path: Path) -> list[str]:
    extension = extract_extension(path)
    return _loaders[extension](path)


def register_loader(loader: str) -> Callable[[LoaderFn], LoaderFn]:
    def decorator(loader_fn: LoaderFn) -> LoaderFn:
        @wraps(loader_fn)
        def wrapper(path: Path) -> list[str]:
            return loader_fn(path)

        _loaders[loader] = wrapper
        return wrapper

    return decorator


@register_loader("txt")
def get_data_from_txt_file(path: Path) -> list[str]:
    with open(path, encoding="utf-8") as file:  # noqa: PTH123
        return file.read().splitlines()
