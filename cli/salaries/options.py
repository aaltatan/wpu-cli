from decimal import Decimal
from pathlib import Path
from typing import Annotated

import typer
from syriantaxes import RoundingMethod

SalariesWorkbookPathArg = Annotated[
    Path,
    typer.Argument(
        help="Path to salaries workbook",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
]

SalariesWorkbookPasswordOpt = Annotated[
    str,
    typer.Option(
        "-p",
        "--password",
        help="Password to open salaries workbook",
        envvar="SALARY_WORKBOOK_PASSWORD",
        prompt=True,
        hide_input=True,
    ),
]

SSRoundToNearestOpt = Annotated[
    Decimal,
    typer.Option(
        "--ss-round-to-nearest",
        help="Round Social Security salary to nearest",
        parser=Decimal,
    ),
]

SSRoundingMethodOpt = Annotated[
    RoundingMethod,
    typer.Option(
        "--ss-rounding-method",
        help="Rounding method for Social Security salary",
    ),
]

CalculationRoundToNearestOpt = Annotated[
    Decimal,
    typer.Option(
        "--calculation-round-to-nearest",
        help="Round calculation to nearest",
        parser=Decimal,
    ),
]

CalculationRoundingMethodOpt = Annotated[
    RoundingMethod,
    typer.Option(
        "--calculation-rounding-method",
        help="Rounding method for calculation",
    ),
]

TaxesRoundToNearestOpt = Annotated[
    Decimal,
    typer.Option(
        "--taxes-round-to-nearest",
        help="Round taxes to nearest",
        parser=Decimal,
    ),
]

TaxesRoundingMethodOpt = Annotated[
    RoundingMethod,
    typer.Option(
        "--taxes-rounding-method",
        help="Rounding method for taxes",
    ),
]

NetBankRoundToNearestOpt = Annotated[
    Decimal,
    typer.Option(
        "--net-bank-round-to-nearest",
        help="Round net bank",
        parser=Decimal,
    ),
]

NetBankRoundingMethodOpt = Annotated[
    RoundingMethod,
    typer.Option(
        "--net-bank-rounding-method",
        help="Rounding method for net bank",
    ),
]

NetCashRoundToNearestOpt = Annotated[
    Decimal,
    typer.Option(
        "--net-cash-round-to-nearest",
        help="Round net cash",
        parser=Decimal,
    ),
]

NetCashRoundingMethodOpt = Annotated[
    RoundingMethod,
    typer.Option(
        "--net-cash-rounding-method",
        help="Rounding method for net cash",
    ),
]

CalculatedStartColumnOpt = Annotated[
    str,
    typer.Option(
        "--calculated-start-column",
        help="Calculated start column",
    ),
]

CalculatedEndColumnOpt = Annotated[
    str,
    typer.Option(
        "--calculated-end-column",
        help="Calculated end column",
    ),
]

StartRowOpt = Annotated[
    int,
    typer.Option(
        "--start-row",
        help="Start row",
        parser=int,
    ),
]

WriteConfirmationOpt = Annotated[
    bool,
    typer.Option(
        "-w",
        "--write-confirmation",
        help="Write confirmation",
    ),
]
