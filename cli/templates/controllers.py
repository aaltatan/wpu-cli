from typing import Annotated

import typer

from .generators import DocxTemplateGenerator
from .loaders import ExcelGroupedDataLoader, ExcelSingleRowDataLoader
from .services import generate_templates, make_output_dir
from .types import (
    DataFilepath,
    FilenameKey,
    IncludeIndexInFilename,
    OutputDirectory,
    TemplatePath,
)

app = typer.Typer()


@app.command(name="xlsx-docx")
def generate_docx_from_xlsx_single_row(
    data_filepath: DataFilepath,
    template: TemplatePath,
    output_dirpath: OutputDirectory = None,
    filename_key: FilenameKey = None,
    include_index_in_filename: IncludeIndexInFilename = False,  # noqa: FBT002
):
    """Generate docx files from xlsx file (single row)."""
    output_dir = make_output_dir(output_dirpath)

    loader = ExcelSingleRowDataLoader(data_filepath)
    generator = DocxTemplateGenerator(
        template,
        output_dir,
        include_index_in_filename=include_index_in_filename,
    )

    generate_templates(loader, generator, filename_key)


@app.command(name="m-xlsx-docx")
def generate_docx_from_xlsx_multiple_rows(  # noqa: PLR0913
    grouped_columns: Annotated[
        list[str],
        typer.Option("--column", "-c", help="Column to be grouped"),
    ],
    data_filepath: DataFilepath,
    template: TemplatePath,
    group_key: Annotated[
        str, typer.Option("--group-key", help="Group key")
    ] = "data",
    output_dirpath: OutputDirectory = None,
    filename_key: FilenameKey = None,
    include_index_in_filename: IncludeIndexInFilename = False,  # noqa: FBT002
):
    """Generate docx files from xlsx file (multiple rows)."""
    output_dir = make_output_dir(output_dirpath)

    loader = ExcelGroupedDataLoader(data_filepath, group_key, *grouped_columns)
    generator = DocxTemplateGenerator(
        template,
        output_dir,
        include_index_in_filename=include_index_in_filename,
    )

    generate_templates(loader, generator, filename_key)
