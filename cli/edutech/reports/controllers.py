from datetime import datetime, timezone
from typing import Annotated

import typer
from devtools import debug
from playwright.sync_api import sync_playwright

from cli.utils import get_authenticated_page

from .services import JournalsPageFilters, get_journals

app = typer.Typer()


@app.command(name="cash")
def generate_cash_report(
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
            prompt=True,
            help="Automata edutech username",
            envvar="EDUTECH_USERNAME",
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            "--password",
            prompt="Automata edutech password",
            help="Automata edutech password",
            hide_input=True,
            envvar="EDUTECH_PASSWORD",
        ),
    ],
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
) -> None:
    """Generate cash report."""
    with sync_playwright() as p:
        authenticated_page = get_authenticated_page(
            p, edutech_username, password
        )

        filters = JournalsPageFilters(
            from_date=datetime(2025, 11, 17, tzinfo=timezone.utc),
            to_date=datetime(2025, 11, 18, tzinfo=timezone.utc),
            accounts=accounts,
        )

        journals = get_journals(
            authenticated_page=authenticated_page,
            timeout=timeout,
            filters=filters,
        )

        debug(journals)
