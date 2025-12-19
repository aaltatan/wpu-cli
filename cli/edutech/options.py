import re
from typing import Annotated

import typer


def validate_financial_year(year: str) -> None:
    pattern = re.compile(r"^20\d{2}/20\d{2}$")

    if not pattern.match(year):
        message = (
            f"Invalid financial year: {year} you should use format 2025/2026"
        )
        raise typer.BadParameter(message, param_hint="--year")

    last_year, current_year = year.split("/")

    if int(last_year) >= int(current_year):
        message = f"Invalid financial year: {year}"
        raise typer.BadParameter(message, param_hint="--year")


FinancialYearOption = Annotated[
    str,
    typer.Option(
        "--year",
        help="Financial year in edutech general accounting",
        prompt="Financial year in edutech general accounting e.g. 2025/2026",
        callback=validate_financial_year,
    ),
]

EdutechPasswordOption = Annotated[
    str,
    typer.Option(
        "--edutech-password",
        prompt="Automata edutech password",
        help="Automata edutech password",
        hide_input=True,
        envvar="EDUTECH_PASSWORD",
    ),
]

EdutechUsernameOption = Annotated[
    str,
    typer.Option(
        "--username",
        prompt="Automata edutech username",
        help="Automata edutech username",
        envvar="EDUTECH_USERNAME",
    ),
]

TimeoutAfterInsertingRowsOption = Annotated[
    int,
    typer.Option(
        "--timeout",
        help="Timeout after inserting rows",
        envvar="EDUTECH_TIMEOUT_AFTER_INSERTING_ROWS",
    ),
]
