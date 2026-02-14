from dataclasses import dataclass

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


@dataclass
class PathOptions:
    data: DataFilepathOpt
    template: TemplateFilepathOpt


@dataclass
class SingleDocxOptions:
    filepath: FilepathOpt
    template_data_variable: TemplateDataVariableOpt
    pdf: PDFOpt = False


@dataclass
class MultipleDocxOptions:
    output_dir: OutputDirOpt
    filename_key: FilenameKeyOpt
    pdf: PDFOpt = False
    include_idx_in_filename: IncludeIndexInFilenameOpt = True


@dataclass
class MultipleRowsXlsxOptions:
    grouped_columns: GroupedColumnsOpt
    group_variable: GroupKeyVariableOpt
