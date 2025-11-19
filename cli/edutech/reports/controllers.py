from datetime import datetime, timezone
from typing import Annotated

import typer
from devtools import debug
from playwright.sync_api import sync_playwright

from cli.edutech.types import EdutechPassword, EdutechUsername, FinancialYear
from cli.edutech.validators import validate_financial_year
from cli.utils import get_authenticated_page

from .services import JournalsPageFilters, get_journals

app = typer.Typer()


@app.command(name="cash")
def generate_cash_report(  # noqa: PLR0913
    edutech_username: EdutechUsername,
    password: EdutechPassword,
    financial_year: FinancialYear,
    accounts: Annotated[
        list[str],
        typer.Option(
            "--accounts",
            "-a",
            help="Accounts to filter journals data by",
            default_factory=lambda: [
                "186208",
                "186209",
                "186210",
            ],
        ),
    ],
    grid_columns: Annotated[
        list[str],
        typer.Option(
            "--columns",
            "-c",
            help="Grid columns to select",
            default_factory=lambda: [
                "tAccountName",
                "tAccountNameCode",
                "tVoucherType",
                "tVoucherNumber",
                "costCenterCol",
                "noteCol",
            ],
        ),
    ],
    from_date: Annotated[
        datetime,
        typer.Option(
            "--from-date",
            help="From date in edutech general accounting",
            prompt="From date in edutech general accounting e.g. 2025-11-17",
        ),
    ],
    to_date: Annotated[
        datetime,
        typer.Option(
            "--to-date",
            help="To date in edutech general accounting",
            default_factory=lambda: datetime.now(timezone.utc),
        ),
    ],
) -> None:
    """Generate cash report."""
    validate_financial_year(financial_year)
    with sync_playwright() as p:
        authenticated_page = get_authenticated_page(
            p, edutech_username, password
        )

        filters = JournalsPageFilters(
            from_date=from_date,
            to_date=to_date,
            accounts=accounts,
            grid_columns=grid_columns,
        )

        journals = get_journals(
            authenticated_page=authenticated_page,
            filters=filters,
            financial_year=financial_year,
        )

        debug(journals)
