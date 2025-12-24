from pathlib import Path

import typer

from cli.fuzz.readers import get_readers
from cli.utils import extract_extension


def reader_path_callback(value: Path) -> Path:
    extension = extract_extension(value)

    if extension not in get_readers():
        message = f"No implementation found for '{extension}' extension"
        raise typer.BadParameter(message)

    return value
