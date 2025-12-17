from collections.abc import Callable
from functools import wraps
from pathlib import Path

from cli.clipboard import get_clipboard

type LoaderFn = Callable[[Path], list[str]]


_loaders: dict[str, LoaderFn] = {}


def get_clipboard_data() -> list[str]:
    clipboard = get_clipboard()
    return [line for line in clipboard.splitlines() if line]


def get_loader_data(path: Path) -> list[str]:
    loader = path.suffix.replace(".", "")

    if loader not in _loaders:
        message = f"Loader '{loader}' not found"
        raise ValueError(message)

    return _loaders[loader](path)


def register_loader(loader: str) -> Callable[[LoaderFn], LoaderFn]:
    def decorator(loader_fn: LoaderFn) -> LoaderFn:
        @wraps(loader_fn)
        def wrapper(path: Path) -> list[str]:
            if not path.is_file():
                message = f"No file found at '{path}'"
                raise ValueError(message)

            if path.suffix != f".{loader}":
                message = f"No loader for '{path.suffix}' was found"
                raise ValueError(message)

            return loader_fn(path)

        _loaders[loader] = wrapper
        return wrapper

    return decorator


@register_loader("txt")
def get_data_from_txt_file(path: Path) -> list[str]:
    with open(path, encoding="utf-8") as file:  # noqa: PTH123
        return file.read().splitlines()
