from typing import Annotated

import typer

FinancialYearOption = Annotated[
    str,
    typer.Option(
        "--year",
        help="Financial year in edutech general accounting",
        prompt="Financial year in edutech general accounting e.g. 2025/2026",
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
        envvar="TIMEOUT_AFTER_INSERTING_ROWS",
    ),
]
