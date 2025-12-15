from typing import Annotated

import typer
from syriantaxes import RoundingMethod

BracketMinsOption = Annotated[
    list[float],
    typer.Option(
        "--brackets-mins",
        default_factory=list,
        envvar="BRACKET_TAX_MINS",
    ),
]

BracketMaxsOption = Annotated[
    list[float],
    typer.Option(
        "--brackets-maxs",
        default_factory=list,
        envvar="BRACKET_TAX_MAXS",
    ),
]

BracketRatesOption = Annotated[
    list[float],
    typer.Option(
        "--brackets-rates",
        default_factory=list,
        envvar="BRACKET_TAX_RATES",
    ),
]

MinAllowedSalaryOption = Annotated[
    float,
    typer.Option(
        "--min-allowed-salary",
        envvar="TAXES_MIN_ALLOWED_SALARY",
    ),
]

TaxesRoundingMethodOption = Annotated[
    RoundingMethod,
    typer.Option(
        "ROUND_HALF_UP",
        "--taxes-rounding-method",
        envvar="TAXES_TAXES_ROUNDING_METHOD",
    ),
]

TaxesRoundToNearestOption = Annotated[
    float,
    typer.Option(
        "--taxes-round-to-nearest",
        envvar="TAXES_TAXES_ROUND_TO_NEAREST",
    ),
]

SsRoundingMethodOption = Annotated[
    RoundingMethod,
    typer.Option(
        "ROUND_HALF_UP",
        "--ss-rounding-method",
        envvar="TAXES_SS_ROUNDING_METHOD",
    ),
]

SsRoundToNearestOption = Annotated[
    float,
    typer.Option(
        "--ss-round-to-nearest",
        envvar="TAXES_SS_ROUND_TO_NEAREST",
    ),
]
