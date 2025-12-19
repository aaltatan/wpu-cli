from pathlib import Path
from typing import Annotated

import typer

DataPathOption = Annotated[
    Path,
    typer.Option(
        "--data-file",
        "-d",
        help="Path to the data file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
]

TemplatePathOption = Annotated[
    Path,
    typer.Option(
        "--template",
        "-t",
        help="Path to the template file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
]

OutputDirOption = Annotated[
    Path | None,
    typer.Option(
        "--output-dir",
        "-o",
        help="Path to the output directory",
        exists=False,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
]

FilenameKeyOption = Annotated[
    str | None,
    typer.Option(
        "-k",
        "--filename-key",
        help="Key to use as filename from data",
        envvar="TEMPLATES_DEFAULT_GENERATED_SINGLE_FILE_NAME",
    ),
]

IncludeIndexInFilenameOption = Annotated[
    bool,
    typer.Option(
        "--include-index",
        help="Include index in filename",
    ),
]

PDFOption = Annotated[
    bool,
    typer.Option(
        "--pdf",
        help="Generate a PDF file for each template",
    ),
]

FilenameOption = Annotated[
    str,
    typer.Option("--filename", help="generated filename"),
]

TemplateDataKeyOption = Annotated[
    str,
    typer.Option(
        "--data-key",
        help="Key to use as data from template, e.g. {%p for item in data['data'] %}",
        envvar="TEMPLATES_DEFAULT_GENERATE_SINGLE_FILE_DATA_KEY",
    ),
]

GroupedColumnsOption = Annotated[
    list[str],
    typer.Option(
        "--column",
        "-c",
        help="Column to be grouped",
        envvar="TEMPLATES_DEFAULT_MULTIPLE_ROWS_GROUPED_KEY",
    ),
]

GroupKey = Annotated[str, typer.Option("--group-key", help="Group key")]
