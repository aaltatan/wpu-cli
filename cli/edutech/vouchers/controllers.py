from pathlib import Path
from typing import Annotated

import typer
from playwright.sync_api import sync_playwright

from cli.edutech.options import (
    EdutechPasswordOption,
    EdutechUsernameOption,
    FinancialYearOption,
    TimeoutAfterInsertingRowsOption,
)
from cli.edutech.services import get_edutech_authenticated_page

from .services import Chapter, add_voucher, get_voucher_from_xlsx

app = typer.Typer()


@app.command()
def add_salaries(  # noqa: PLR0913
    timeout_after_inserting_rows: TimeoutAfterInsertingRowsOption,
    edutech_username: EdutechUsernameOption,
    password: EdutechPasswordOption,
    financial_year: FinancialYearOption,
    filepath: Annotated[
        Path,
        typer.Option(
            "-p",
            "--filepath",
            help="Path to Salaries file",
            exists=True,
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
        ),
    ],
    chapter: Annotated[
        Chapter,
        typer.Option("--chapter", help="Chapter of the Salaries.xlsb file"),
    ],
):
    rows = get_voucher_from_xlsx(filepath, chapter)
    with sync_playwright() as playwright:
        authenticated_page = get_edutech_authenticated_page(playwright, edutech_username, password)
        add_voucher(
            authenticated_page,
            rows,
            financial_year,
            timeout_after_inserting_rows,
        )
