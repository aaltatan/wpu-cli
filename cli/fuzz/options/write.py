from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from cli.fuzz.writers import Writer


def export_path_callback(path: Path) -> Path:
    if path.exists():
        message = f"The file {path} already exists."
        raise typer.BadParameter(message)

    return path


ExportPathOpt = Annotated[
    Path,
    typer.Option(
        "-e",
        "--export-path",
        help="Path to the output file",
        exists=False,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        callback=export_path_callback,
    ),
]

WriterOpt = Annotated[
    Writer,
    typer.Option(
        "-w",
        "--writer",
        envvar="FUZZ_DEFAULT_WRITER",
        help="writer type",
    ),
]


@dataclass
class WriteOptions:
    export_path: ExportPathOpt
    writer: WriterOpt
