from pathlib import Path

import typer

from cli.fuzz.loaders import get_loaders
from cli.utils import extract_extension


def loader_path_callback(value: Path) -> Path:
    extension = extract_extension(value)

    if extension not in get_loaders():
        message = f"No implementation found for '{extension}' extension"
        raise typer.BadParameter(message)

    return value
