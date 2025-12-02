from collections.abc import Collection
from pathlib import Path
from typing import Annotated, Any

import typer

type Data = Collection[dict[Any, Any]]

DataFilepath = Annotated[
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

TemplatePath = Annotated[
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

OutputDirectory = Annotated[
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

FilenameKey = Annotated[
    str | None,
    typer.Option(
        "--filename-key",
        "-k",
        help="Key to use as filename from data",
    ),
]

IncludeIndexInFilename = Annotated[
    bool,
    typer.Option(
        "--include-index",
        help="Include index in filename",
    ),
]

PDF = Annotated[
    bool,
    typer.Option(
        "--pdf",
        help="Generate a PDF file for each template",
    ),
]

Filename = Annotated[
    str,
    typer.Option("--filename", help="generated filename"),
]

TemplateDataKey = Annotated[
    str,
    typer.Option(
        "--data-key",
        help="Key to use as data from template, e.g. {%p for item in data['data'] %}",  # noqa: E501
    ),
]

GroupedColumns = Annotated[
    list[str],
    typer.Option("--column", "-c", help="Column to be grouped"),
]

GroupKey = Annotated[str, typer.Option("--group-key", help="Group key")]
