from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from .enums import Chapter

TimeoutAfterInsertingRowsOpt = Annotated[
    int,
    typer.Option(
        "--timeout",
        help="Timeout after inserting rows",
        envvar="EDUTECH_TIMEOUT_AFTER_INSERTING_ROWS",
    ),
]

VoucherFilepathOpt = Annotated[
    Path,
    typer.Option(
        "-p",
        "--filepath",
        help="Path to voucher file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
]

ChapterOpt = Annotated[
    Chapter,
    typer.Option(
        "--chapter",
        help="Chapter of the Salaries.xlsb file",
    ),
]


@dataclass
class AddVouchersOptions:
    filepath: VoucherFilepathOpt
    chapter: ChapterOpt
    timeout_after_inserting_rows: TimeoutAfterInsertingRowsOpt
