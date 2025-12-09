# ruff: noqa: FBT002, PLR0913

import typer

from .generators import (
    MultipleDocxTemplateGenerator,
    SingleDocxTemplateGenerator,
)
from .help import HELP_TEXT
from .loaders import ExcelGroupedDataLoader, ExcelSingleRowDataLoader
from .options import (
    DataPathOption,
    FilenameKeyOption,
    FilenameOption,
    GroupedColumnsOption,
    GroupKey,
    IncludeIndexInFilenameOption,
    OutputDirPathOption,
    PDFOption,
    TemplateDataKeyOption,
    TemplatePathOption,
)
from .services import generate_templates, make_output_dir

DEFAULT_FILENAME = "output"
DEFAULT_DATA_KEY = "data"
DEFAULT_GROUP_KEY = "data"
DEFAULT_OUTPUT_DESKTOP_DIRNAME = "output"


app = typer.Typer(help=HELP_TEXT)


@app.command(name="xlsx2mdocx")
def generate_multiple_docx_files_from_xlsx_single_row(
    data_filepath: DataPathOption,
    template: TemplatePathOption,
    output_dirpath: OutputDirPathOption = None,
    filename_key: FilenameKeyOption = None,
    pdf: PDFOption = False,
    include_index_in_filename: IncludeIndexInFilenameOption = False,
):
    """Generate multiple docx files from xlsx file (single row)."""
    output_dir = make_output_dir(DEFAULT_OUTPUT_DESKTOP_DIRNAME, output_dirpath)

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
    data_filepath: DataPathOption,
    template: TemplatePathOption,
    filename: FilenameOption = DEFAULT_FILENAME,
    template_data_key: TemplateDataKeyOption = DEFAULT_DATA_KEY,
    output_dirpath: OutputDirPathOption = None,
    pdf: PDFOption = False,
):
    """Generate single docx file from xlsx file (single row)."""
    output_dir = make_output_dir(DEFAULT_OUTPUT_DESKTOP_DIRNAME, output_dirpath)

    loader = ExcelSingleRowDataLoader(data_filepath)
    generator = SingleDocxTemplateGenerator(
        template, output_dir, filename, template_data_key, pdf=pdf
    )

    generate_templates(loader, generator)


@app.command(name="mxlsx2mdocx")
def generate_docx_multiple_files_from_xlsx_multiple_rows(
    grouped_columns: GroupedColumnsOption,
    data_filepath: DataPathOption,
    template: TemplatePathOption,
    group_key: GroupKey = DEFAULT_GROUP_KEY,
    output_dirpath: OutputDirPathOption = None,
    filename_key: FilenameKeyOption = None,
    include_index_in_filename: IncludeIndexInFilenameOption = False,
    pdf: PDFOption = False,
):
    """Generate multiple docx files from xlsx file (multiple rows)."""
    output_dir = make_output_dir(DEFAULT_OUTPUT_DESKTOP_DIRNAME, output_dirpath)

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
    grouped_columns: GroupedColumnsOption,
    data_filepath: DataPathOption,
    template: TemplatePathOption,
    filename: FilenameOption = DEFAULT_FILENAME,
    template_data_key: TemplateDataKeyOption = DEFAULT_DATA_KEY,
    group_key: GroupKey = DEFAULT_GROUP_KEY,
    output_dirpath: OutputDirPathOption = None,
    pdf: PDFOption = False,
):
    """Generate single docx file from xlsx file (multiple rows)."""
    output_dir = make_output_dir(DEFAULT_OUTPUT_DESKTOP_DIRNAME, output_dirpath)

    loader = ExcelGroupedDataLoader(data_filepath, group_key, *grouped_columns)
    generator = SingleDocxTemplateGenerator(
        template, output_dir, filename, template_data_key, pdf=pdf
    )

    generate_templates(loader, generator)
