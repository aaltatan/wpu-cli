from decimal import Decimal
from pathlib import Path
from typing import Annotated

import typer
from syriantaxes import RoundingMethod

SalariesFilePathArg = Annotated[
    Path,
    typer.Argument(
        help="Path to salaries file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
]

SalariesFilePasswordOpt = Annotated[
    str,
    typer.Option(
        "--password",
        help="Password to open salaries file",
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

StartRowOpt = Annotated[
    int,
    typer.Option(
        "--start-row",
        help="Start row",
    ),
]
