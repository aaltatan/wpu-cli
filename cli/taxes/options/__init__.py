from pathlib import Path
from typing import Annotated

import typer

from cli.taxes.exporters import get_export_functions
from cli.utils import extract_extension

from .ar import AmountRange, get_amount_range
from .common import Options, get_options
from .ss import SocialSecuritySalaryOption, get_ss_obj

__all__ = [
    "AmountRange",
    "Options",
    "SocialSecuritySalaryOption",
    "get_amount_range",
    "get_options",
    "get_ss_obj",
]

GrossSalaryArgument = Annotated[float, typer.Argument()]

GrossCompensationsArgument = Annotated[float, typer.Argument()]

TargetSalaryArgument = Annotated[float, typer.Argument()]

CompensationsRateOption = Annotated[
    float,
    typer.Option(
        "-r",
        "--compensations-rate",
        envvar="TAXES_DEFAULT_COMPENSATIONS_RATE",
    ),
]


def export_path_callback(value: Path | None) -> Path | None:
    if value:
        if value.exists():
            message = f"The file {value} already exists."
            raise typer.BadParameter(message)

        extension = extract_extension(value)

        if extension not in get_export_functions():
            message = f"extension of type (.{extension}) not supported."
            raise typer.BadParameter(message)

    return value


ExportPathOption = Annotated[
    Path | None,
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
