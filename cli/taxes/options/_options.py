from pathlib import Path
from typing import Annotated

import typer

from cli.taxes.writers import get_write_functions
from cli.utils import extract_extension

CompensationsRateOpt = Annotated[
    float,
    typer.Option(
        "-r",
        "--compensations-rate",
        envvar="TAXES_DEFAULT_COMPENSATIONS_RATE",
    ),
]


def write_path_callback(value: Path | None) -> Path | None:
    if value:
        if value.exists():
            message = f"The file {value} already exists."
            raise typer.BadParameter(message)

        extension = extract_extension(value)

        if extension not in get_write_functions():
            message = f"extension of type (.{extension}) not supported."
            raise typer.BadParameter(message)

    return value


WritePathOpt = Annotated[
    Path | None,
    typer.Option(
        "-e",
        "--write-path",
        help="Path to the output file",
        exists=False,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        callback=write_path_callback,
    ),
]
