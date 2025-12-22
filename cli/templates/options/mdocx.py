from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from .common import PDFOpt

RICH_HELP_PANEL = "Multiple Docx Options"

FilenameKeyOpt = Annotated[
    str,
    typer.Option(
        "-k",
        "--filename-key",
        help="Keyname (column name) to use its value in generated filename",
        rich_help_panel=RICH_HELP_PANEL,
    ),
]

IncludeIndexInFilenameOpt = Annotated[
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
        callback=create_output_dir,
        rich_help_panel=RICH_HELP_PANEL,
    ),
]


@dataclass
class MultipleDocxOptions:
    output_dir: OutputDirOpt
    filename_key: FilenameKeyOpt
    include_idx_in_filename: IncludeIndexInFilenameOpt
    pdf: PDFOpt
