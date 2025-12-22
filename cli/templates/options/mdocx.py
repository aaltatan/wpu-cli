from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from .common import PDFOption

RICH_HELP_PANEL = "Multiple Docx Options"

FilenameKeyOption = Annotated[
    str,
    typer.Option(
        "-k",
        "--filename-key",
        help="Keyname (column name) to use its value in generated filename",
        rich_help_panel=RICH_HELP_PANEL,
    ),
]

IncludeIndexInFilenameOption = Annotated[
    bool,
    typer.Option(
        "-i",
        "--include-index",
        help="Include index in generated filename e.g.: 1 - <your_filename>.docx",
        rich_help_panel=RICH_HELP_PANEL,
    ),
]


def create_output_dir(output_dir: Path) -> Path:
    if not output_dir.exists():
        output_dir.absolute().mkdir(parents=True)

    return output_dir


OutputDirOption = Annotated[
    Path,
    typer.Option(
        "-o",
        "--output-dirpath",
        help="Path to the output directory",
        exists=False,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        callback=create_output_dir,
        rich_help_panel=RICH_HELP_PANEL,
    ),
]


@dataclass
class MultipleDocxOptions:
    output_dir: OutputDirOption
    filename_key: FilenameKeyOption
    include_idx_in_filename: IncludeIndexInFilenameOption
    pdf: PDFOption


def get_multiple_docx_options(
    output_dir: OutputDirOption,
    filename_key: FilenameKeyOption,
    *,
    include_idx_in_filename: IncludeIndexInFilenameOption = True,
    pdf: PDFOption = False,
) -> MultipleDocxOptions:
    return MultipleDocxOptions(output_dir, filename_key, include_idx_in_filename, pdf)
