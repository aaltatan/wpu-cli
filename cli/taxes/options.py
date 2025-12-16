from typing import Annotated

import typer
from syriantaxes import RoundingMethod

BracketMinsOption = Annotated[
    list[float],
    typer.Option(
        "--brackets-mins",
        default_factory=list,
        envvar="TAXES_BRACKET_TAX_MINS",
    ),
]

BracketMaxesOption = Annotated[
    list[float],
    typer.Option(
        "--brackets-maxs",
        default_factory=list,
        envvar="TAXES_BRACKET_TAX_MAXS",
    ),
]

BracketRatesOption = Annotated[
    list[float],
    typer.Option(
        "--brackets-rates",
        default_factory=list,
        envvar="TAXES_BRACKET_TAX_RATES",
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

MinSsAllowedSalaryOption = Annotated[
    float,
    typer.Option(
        "--min-ss-allowed-salary",
        envvar="TAXES_MIN_SS_ALLOWED_SALARY",
    ),
]

SsDeductionRateOption = Annotated[
    float,
    typer.Option(
        "--ss-deduction-rate",
        envvar="TAXES_DEFAULT_SS_DEDUCTION_RATE",
    ),
]

SocialSecuritySalaryOption = Annotated[
    float | None,
    typer.Option(
        "--ss",
        "--social-security-salary",
    ),
]

FixedTaxRateOption = Annotated[
    float,
    typer.Option(
        "--fixed-tax-rate",
        envvar="TAXES_FIXED_TAX_RATE",
    ),
]

GrossSalaryArgument = Annotated[float, typer.Argument()]

GrossCompensationsOption = Annotated[
    float,
    typer.Option(
        "-c",
        "--gross-compensations",
    ),
]

TargetSalaryArgument = Annotated[float, typer.Argument()]

CompensationsRateOption = Annotated[
    float,
    typer.Option(
        "-r",
        "--compensations-rate",
        envvar="DEFAULT_COMPENSATIONS_RATE",
    ),
]
