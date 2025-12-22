from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer


class Chapter(StrEnum):
    ONE = "1"
    TWO = "2"
    THREE = "3"

    def __str__(self) -> str:
        return self.value


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


def get_add_vouchers_options(
    filepath: VoucherFilepathOpt,
    chapter: ChapterOpt,
    timeout_after_inserting_rows: TimeoutAfterInsertingRowsOpt,
) -> AddVouchersOptions:
    return AddVouchersOptions(filepath, chapter, timeout_after_inserting_rows)
