from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

RICH_HELP_PANEL = "Common Options"

DataFilepathOption = Annotated[
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

TemplateFilepathOption = Annotated[
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


PDFOption = Annotated[
    bool,
    typer.Option(
        "--pdf",
        help="Generate a PDF file(s)",
        rich_help_panel="PDF",
        expose_value=True,
    ),
]


@dataclass
class Options:
    data_filepath: DataFilepathOption
    template_filepath: TemplateFilepathOption


def get_options(
    data_filepath: DataFilepathOption, template_filepath: TemplateFilepathOption
) -> Options:
    return Options(data_filepath, template_filepath)
