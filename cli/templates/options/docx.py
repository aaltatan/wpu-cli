from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from ._options import PDFOpt

RICH_HELP_PANEL = "Single Docx Options"


def filepath_callback(value: Path) -> Path:
    if value.exists():
        message = f"The file {value} already exists."
        raise typer.BadParameter(message)

    return value


FilepathOpt = Annotated[
    Path,
    typer.Option(
        "-o",
        "--output-filepath",
        help="Path to the output file",
        exists=False,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        callback=filepath_callback,
        rich_help_panel=RICH_HELP_PANEL,
    ),
]


TemplateDataVariableOpt = Annotated[
    str,
    typer.Option(
        "-v",
        "--template-data-variable",
        help=(
            "Iterable variable to use it in template"
            "e.g.:"
            "if its value is 'data' then you will use it in the template like this:"
            "{%p for item in data %}"
            "..."
            " {{ page_break }} "
            "{%p endfor %}"
        ),
        envvar="TEMPLATES_DEFAULT_SINGLE_DOCX_TEMPLATE_DATA_VARIABLE",
        rich_help_panel=RICH_HELP_PANEL,
    ),
]


@dataclass
class SingleDocxOptions:
    filepath: FilepathOpt
    template_data_variable: TemplateDataVariableOpt
    pdf: PDFOpt
