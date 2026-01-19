from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

RICH_HELP_PANEL = "Common Options"

DataFilepathOpt = Annotated[
    Path,
    typer.Option(
        "-d",
        "--data-filepath",
        help="Path to the data file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        rich_help_panel=RICH_HELP_PANEL,
    ),
]

TemplateFilepathOpt = Annotated[
    Path,
    typer.Option(
        "-t",
        "--template-filepath",
        help="Path to the template file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        rich_help_panel=RICH_HELP_PANEL,
    ),
]


@dataclass
class PathOptions:
    data: DataFilepathOpt
    template: TemplateFilepathOpt
