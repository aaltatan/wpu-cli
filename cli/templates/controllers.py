# ruff: noqa: FBT002, PLR0913

from typing import Annotated

import typer

from .generators import (
    MultipleDocxTemplateGenerator,
    SingleDocxTemplateGenerator,
)
from .help import HELP_TEXT
from .loaders import ExcelGroupedDataLoader, ExcelSingleRowDataLoader
from .services import generate_templates, make_output_dir
from .types import (
    PDF,
    DataFilepath,
    DataKey,
    Filename,
    FilenameKey,
    IncludeIndexInFilename,
    OutputDirectory,
    TemplatePath,
)

DEFAULT_FILENAME = "output"
DEFAULT_DATA_KEY = "data"
DEFAULT_GROUP_KEY = "data"


app = typer.Typer(
    help=HELP_TEXT,
)


@app.command(name="xlsx2mdocx")
def generate_multiple_docx_files_from_xlsx_single_row(
    data_filepath: DataFilepath,
    template: TemplatePath,
    output_dirpath: OutputDirectory = None,
    filename_key: FilenameKey = None,
    pdf: PDF = False,
    include_index_in_filename: IncludeIndexInFilename = False,
):
    """Generate multiple docx files from xlsx file (single row)."""
    output_dir = make_output_dir(output_dirpath)

    loader = ExcelSingleRowDataLoader(data_filepath)
    generator = MultipleDocxTemplateGenerator(
        template,
        output_dir,
        filename_key,
        pdf=pdf,
        include_index_in_filename=include_index_in_filename,
    )

    generate_templates(loader, generator)


@app.command(name="xlsx2docx")
def generate_single_docx_file_from_xlsx_single_row(
    data_filepath: DataFilepath,
    template: TemplatePath,
    filename: Filename = DEFAULT_FILENAME,
    data_key: DataKey = DEFAULT_DATA_KEY,
    output_dirpath: OutputDirectory = None,
    pdf: PDF = False,
):
    """Generate single docx file from xlsx file (single row)."""
    output_dir = make_output_dir(output_dirpath)

    loader = ExcelSingleRowDataLoader(data_filepath)
    generator = SingleDocxTemplateGenerator(
        template, output_dir, filename, data_key, pdf=pdf
    )

    generate_templates(loader, generator)


@app.command(name="mxlsx2mdocx")
def generate_docx_multiple_files_from_xlsx_multiple_rows(
    grouped_columns: Annotated[
        list[str],
        typer.Option("--column", "-c", help="Column to be grouped"),
    ],
    data_filepath: DataFilepath,
    template: TemplatePath,
    group_key: Annotated[
        str, typer.Option("--group-key", help="Group key")
    ] = DEFAULT_GROUP_KEY,
    output_dirpath: OutputDirectory = None,
    filename_key: FilenameKey = None,
    include_index_in_filename: IncludeIndexInFilename = False,
    pdf: PDF = False,
):
    """Generate multiple docx files from xlsx file (multiple rows)."""
    output_dir = make_output_dir(output_dirpath)

    loader = ExcelGroupedDataLoader(data_filepath, group_key, *grouped_columns)
    generator = MultipleDocxTemplateGenerator(
        template,
        output_dir,
        filename_key,
        pdf=pdf,
        include_index_in_filename=include_index_in_filename,
    )

    generate_templates(loader, generator)


@app.command(name="mxlsx2docx")
def generate_single_docx_file_from_xlsx_multiple_rows(
    grouped_columns: Annotated[
        list[str],
        typer.Option("--column", "-c", help="Column to be grouped"),
    ],
    data_filepath: DataFilepath,
    template: TemplatePath,
    filename: Filename = DEFAULT_FILENAME,
    data_key: DataKey = DEFAULT_DATA_KEY,
    group_key: Annotated[
        str, typer.Option("--group-key", help="Group key")
    ] = DEFAULT_GROUP_KEY,
    output_dirpath: OutputDirectory = None,
    pdf: PDF = False,
):
    """Generate single docx file from xlsx file (multiple rows)."""
    output_dir = make_output_dir(output_dirpath)

    loader = ExcelGroupedDataLoader(data_filepath, group_key, *grouped_columns)
    generator = SingleDocxTemplateGenerator(
        template, output_dir, filename, data_key, pdf=pdf
    )

    generate_templates(loader, generator)
