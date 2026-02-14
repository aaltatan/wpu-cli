from pathlib import Path
from typing import Annotated

import typer

from .callbacks import create_output_dir_callback, filepath_callback

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
        rich_help_panel="Common Options",
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
        rich_help_panel="Common Options",
    ),
]


PDFOpt = Annotated[
    bool,
    typer.Option(
        "--pdf",
        help="Generate a PDF file(s)",
        rich_help_panel="PDF",
        expose_value=True,
    ),
]


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
        default_factory=lambda: Path.cwd().home() / "outputs",
        callback=filepath_callback,
        rich_help_panel="Single Docx Options",
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
        rich_help_panel="Single Docx Options",
    ),
]

FilenameKeyOpt = Annotated[
    str,
    typer.Option(
        "-k",
        "--filename-key",
        help="Keyname (column name) to use its value in generated filename",
        rich_help_panel="Multiple Docx Options",
    ),
]

IncludeIndexInFilenameOpt = Annotated[
    bool,
    typer.Option(
        "-i",
        "--include-index",
        help="Include index in generated filename e.g.: 1 - <your_filename>.docx",
        rich_help_panel="Multiple Docx Options",
    ),
]


OutputDirOpt = Annotated[
    Path,
    typer.Option(
        "-o",
        "--output-dirpath",
        help="Path to the output directory",
        exists=False,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        callback=create_output_dir_callback,
        rich_help_panel="Multiple Docx Options",
    ),
]

GroupedColumnsOpt = Annotated[
    list[str],
    typer.Option(
        "-c",
        "--column",
        help="Column to be grouped by",
        rich_help_panel="Multiple Rows xlsx Options",
    ),
]

GroupKeyVariableOpt = Annotated[
    str,
    typer.Option(
        "-g",
        "--group-variable",
        help="Group (Iterable) variable to use it in template e.g.: {%p for item in data %}",
        envvar="TEMPLATES_DEFAULT_XLSX_MULTIPLE_ROWS_TEMPLATE_GROUP_VARIABLE",
        rich_help_panel="Multiple Rows xlsx Options",
    ),
]
