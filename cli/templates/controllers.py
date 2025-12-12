# ruff: noqa: FBT002

import typer

from .callbacks import app_callback
from .loaders import ExcelGroupedDataLoader, ExcelSingleRowDataLoader
from .options import (
    FilenameKeyOption,
    FilenameOption,
    GroupedColumnsOption,
    GroupKey,
    IncludeIndexInFilenameOption,
    TemplateDataKeyOption,
)
from .services import write_templates
from .writers import MultipleDocxTemplateWriter, SingleDocxTemplateWriter

app = typer.Typer(callback=app_callback)


@app.command(name="xlsx2mdocx")
def generate_multiple_docx_files_from_xlsx_single_row(
    ctx: typer.Context,
    filename_key: FilenameKeyOption = None,
    include_index_in_filename: IncludeIndexInFilenameOption = False,
):
    """Generate multiple docx files from xlsx file (single row)."""
    loader = ExcelSingleRowDataLoader(ctx.obj["data_filepath"])
    writer = MultipleDocxTemplateWriter(
        ctx.obj["template"],
        ctx.obj["output_dir"],
        filename_key,
        pdf=ctx.obj["pdf"],
        include_index_in_filename=include_index_in_filename,
    )

    write_templates(loader, writer)


@app.command(name="xlsx2docx")
def generate_single_docx_file_from_xlsx_single_row(
    ctx: typer.Context,
    filename: FilenameOption,
    template_data_key: TemplateDataKeyOption,
):
    """Generate single docx file from xlsx file (single row)."""
    loader = ExcelSingleRowDataLoader(ctx.obj["data_filepath"])
    writer = SingleDocxTemplateWriter(
        ctx.obj["template"],
        ctx.obj["output_dir"],
        filename,
        template_data_key,
        pdf=ctx.obj["pdf"],
    )

    write_templates(loader, writer)


@app.command(name="mxlsx2mdocx")
def generate_docx_multiple_files_from_xlsx_multiple_rows(
    ctx: typer.Context,
    grouped_columns: GroupedColumnsOption,
    group_key: GroupKey,
    filename_key: FilenameKeyOption = None,
    include_index_in_filename: IncludeIndexInFilenameOption = False,
):
    """Generate multiple docx files from xlsx file (multiple rows)."""
    loader = ExcelGroupedDataLoader(
        ctx.obj["data_filepath"], group_key, *grouped_columns
    )
    write = MultipleDocxTemplateWriter(
        ctx.obj["template"],
        ctx.obj["output_dir"],
        filename_key,
        pdf=ctx.obj["pdf"],
        include_index_in_filename=include_index_in_filename,
    )

    write_templates(loader, write)


@app.command(name="mxlsx2docx")
def generate_single_docx_file_from_xlsx_multiple_rows(
    ctx: typer.Context,
    grouped_columns: GroupedColumnsOption,
    filename: FilenameOption,
    template_data_key: TemplateDataKeyOption,
    group_key: GroupKey,
):
    """Generate single docx file from xlsx file (multiple rows)."""
    loader = ExcelGroupedDataLoader(
        ctx.obj["data_filepath"], group_key, *grouped_columns
    )
    writer = SingleDocxTemplateWriter(
        ctx.obj["template"],
        ctx.obj["output_dir"],
        filename,
        template_data_key,
        pdf=ctx.obj["pdf"],
    )

    write_templates(loader, writer)
