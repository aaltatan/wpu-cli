from typing import Annotated

import typer
from playwright.sync_api import sync_playwright

from cli.edutech.options import (
    EdutechPasswordOption,
    EdutechUsernameOption,
    ExcelPasswordOption,
    FinancialYearOption,
    TimeoutOption,
)
from cli.edutech.validators import validate_financial_year
from cli.utils import get_authenticated_page, get_salaries_filepath

from .services import Chapter, add_voucher, get_salaries_voucher_rows

app = typer.Typer()


@app.command()
def add_salaries(  # noqa: PLR0913
    timeout: TimeoutOption,
    edutech_username: EdutechUsernameOption,
    password: EdutechPasswordOption,
    financial_year: FinancialYearOption,
    excel_password: ExcelPasswordOption,
    chapter: Annotated[
        Chapter,
        typer.Option("--chapter", help="Chapter of the Salaries.xlsb file"),
    ],
    start_cell: Annotated[
        tuple[int, int],
        typer.Option("--start-cell", help="Start cell in Salaries.xlsb file"),
    ] = (1, 2),
    last_column: Annotated[
        int,
        typer.Option("--last-column", help="Last column in Salaries.xlsb file"),
    ] = 7,
    sheet_name: Annotated[
        str,
        typer.Option("--sheet", help="Sheet name in Salaries.xlsb file"),
    ] = "Journal Entry Template",
):
    """Add from `Journal Entry Template` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file."""  # noqa: E501
    validate_financial_year(financial_year)
    filepath = get_salaries_filepath()
    rows = get_salaries_voucher_rows(
        filepath,
        password=excel_password,
        chapter=chapter,
        start_cell=start_cell,
        last_column=last_column,
        sheet_name=sheet_name,
    )
    with sync_playwright() as p:
        authenticated_page = get_authenticated_page(
            p, edutech_username, password
        )
        add_voucher(authenticated_page, timeout, rows, financial_year)
