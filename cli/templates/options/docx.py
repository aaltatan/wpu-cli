from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from .common import PDFOption

RICH_HELP_PANEL = "Single Docx Options"


def filepath_callback(value: Path) -> Path:
    if value.exists():
        message = f"The file {value} already exists."
        raise typer.BadParameter(message)

    return value


FilepathOption = Annotated[
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


TemplateDataVariableOption = Annotated[
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
    filepath: FilepathOption
    template_data_variable: TemplateDataVariableOption
    pdf: PDFOption


def get_single_docx_options(
    filepath: FilepathOption,
    template_data_variable: TemplateDataVariableOption,
    *,
    pdf: PDFOption = False,
) -> SingleDocxOptions:
    return SingleDocxOptions(filepath, template_data_variable, pdf)
