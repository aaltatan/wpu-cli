from enum import StrEnum
from typing import Annotated

import typer

from cli.utils import get_salaries_filepath

from .services import add_voucher, get_salaries_voucher_data


class Chapter(StrEnum):
    ONE = "1"
    TWO = "2"
    THREE = "3"


app = typer.Typer()


@app.command()
def add_salaries(  # noqa: PLR0913
    timeout: Annotated[
        int,
        typer.Option(
            "--timeout",
            "-t",
            help="Timeout for playwright",
            envvar="PLAYWRIGHT_TIMEOUT",
        ),
    ],
    edutech_username: Annotated[
        str,
        typer.Option(
            "--edutech-username",
            "-u",
            prompt=True,
            help="Automata edutech username",
            envvar="EDUTECH_USERNAME",
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            "--password",
            "-p",
            prompt=True,
            help="Automata edutech password",
            hide_input=True,
            envvar="EDUTECH_PASSWORD",
        ),
    ],
    excel_password: Annotated[
        str,
        typer.Option(
            "--excel-password",
            "-e",
            prompt=True,
            help="Excel file password",
            hide_input=True,
            envvar="EXCEL_FILE_PASSWORD",
        ),
    ],
    chapter: Annotated[
        Chapter,
        typer.Option(
            "--chapter",
            "-c",
            help="Chapter of the Salaries.xlsb file",
        ),
    ] = Chapter.ONE,
    start_cell: Annotated[
        tuple[int, int],
        typer.Option(
            "--start-cell", "-f", help="Start cell in Salaries.xlsb file"
        ),
    ] = (1, 2),
    last_column: Annotated[
        int,
        typer.Option(
            "--last-column", "-l", help="Last column in Salaries.xlsb file"
        ),
    ] = 7,
    sheet_name: Annotated[
        str,
        typer.Option("--sheet", "-s", help="Sheet name in Salaries.xlsb file"),
    ] = "Journal Entry Template",
):
    """Add from `Journal Entry Template` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file."""  # noqa: E501
    filepath = get_salaries_filepath()
    data = get_salaries_voucher_data(
        filepath,
        password=excel_password,
        chapter=chapter,
        start_cell=start_cell,
        last_column=last_column,
        sheet_name=sheet_name,
    )
    add_voucher(timeout, data, username=edutech_username, password=password)
