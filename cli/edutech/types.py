from typing import Annotated

import typer

FinancialYear = Annotated[
    str,
    typer.Option(
        "--year",
        help="Financial year in edutech general accounting",
        prompt="Financial year in edutech general accounting e.g. 2025/2026",
    ),
]

EdutechPassword = Annotated[
    str,
    typer.Option(
        "--edutech-password",
        prompt="Automata edutech password",
        help="Automata edutech password",
        hide_input=True,
        envvar="EDUTECH_PASSWORD",
    ),
]

ExcelPassword = Annotated[
    str,
    typer.Option(
        "--excel-password",
        prompt="Excel file password",
        help="Excel file password",
        hide_input=True,
        envvar="EXCEL_FILE_PASSWORD",
    ),
]

EdutechUsername = Annotated[
    str,
    typer.Option(
        "--username",
        prompt="Automata edutech username",
        help="Automata edutech username",
        envvar="EDUTECH_USERNAME",
    ),
]

Timeout = Annotated[
    int,
    typer.Option(
        "--timeout",
        help="Timeout for playwright",
        envvar="PLAYWRIGHT_TIMEOUT",
    ),
]
