from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from typer_di import Depends

from .enums import Chapter
from .readers import read_voucher_from_xlsx
from .schemas import Row

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


def _read_voucher_from_xlsx_wrapper(filepath: VoucherFilepathOpt, chapter: ChapterOpt) -> list[Row]:
    return read_voucher_from_xlsx(filepath, chapter)


@dataclass
class AddVouchersOptions:
    timeout_after_inserting_rows: TimeoutAfterInsertingRowsOpt
    rows: list[Row] = Depends(_read_voucher_from_xlsx_wrapper)  # noqa: RUF009
