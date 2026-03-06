# ruff: noqa: FBT002

from .options import (
    DataFilepathOpt,
    FilenameKeyOpt,
    FilepathOpt,
    GroupedColumnsOpt,
    GroupKeyVariableOpt,
    IncludeIndexInFilenameOpt,
    OutputDirOpt,
    PDFOpt,
    TemplateDataVariableOpt,
    TemplateFilepathOpt,
)
from .readers import ExcelGroupedDataReader, ExcelSingleRowDataReader
from .writers import MultipleDocxTemplateWriter, SingleDocxTemplateWriter


def get_excel_single_row_reader(data: DataFilepathOpt) -> ExcelSingleRowDataReader:
    return ExcelSingleRowDataReader(data)


def get_excel_multiple_rows_reader(
    data: DataFilepathOpt,
    grouped_columns: GroupedColumnsOpt,
    group_variable: GroupKeyVariableOpt,
) -> ExcelGroupedDataReader:
    return ExcelGroupedDataReader(data, group_variable, *grouped_columns)


def get_excel_multiple_rows_writer(
    template: TemplateFilepathOpt,
    output_dir: OutputDirOpt,
    filename_key: FilenameKeyOpt,
    pdf: PDFOpt = False,
    include_index_in_filename: IncludeIndexInFilenameOpt = True,
) -> MultipleDocxTemplateWriter:
    return MultipleDocxTemplateWriter(
        template,
        output_dir,
        filename_key,
        pdf=pdf,
        include_index_in_filename=include_index_in_filename,
    )


def get_excel_single_row_writer(
    template: TemplateFilepathOpt,
    filepath: FilepathOpt,
    template_data_variable: TemplateDataVariableOpt,
    pdf: PDFOpt = False,
) -> SingleDocxTemplateWriter:
    return SingleDocxTemplateWriter(template, filepath, template_data_variable, pdf=pdf)
