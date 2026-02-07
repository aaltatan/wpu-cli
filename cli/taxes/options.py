from pathlib import Path
from typing import Annotated

import typer
from syriantaxes import RoundingMethod

from .callbacks import (
    amount_range_start_callback,
    amount_range_step_callback,
    amount_range_stop_callback,
    ss_salary_callback,
    write_path_callback,
)

CompensationsRateOpt = Annotated[
    float,
    typer.Option(
        "-r",
        "--compensations-rate",
        envvar="TAXES_DEFAULT_COMPENSATIONS_RATE",
    ),
]

StartAmountRangeArg = Annotated[float, typer.Argument(callback=amount_range_start_callback)]
StopAmountRangeArg = Annotated[float | None, typer.Argument(callback=amount_range_stop_callback)]
StepAmountRangeArg = Annotated[float | None, typer.Argument(callback=amount_range_step_callback)]

BracketMinsOpt = Annotated[
    list[float],
    typer.Option(
        "--brackets-mins",
        default_factory=list,
        envvar="TAXES_BRACKET_TAX_MINS",
        rich_help_panel="Brackets",
    ),
]
BracketMaxesOpt = Annotated[
    list[float],
    typer.Option(
        "--brackets-maxs",
        default_factory=list,
        envvar="TAXES_BRACKET_TAX_MAXS",
        rich_help_panel="Brackets",
    ),
]
BracketRatesOpt = Annotated[
    list[float],
    typer.Option(
        "--brackets-rates",
        default_factory=list,
        envvar="TAXES_BRACKET_TAX_RATES",
        rich_help_panel="Brackets",
    ),
]


TaxesRoundingMethodOpt = Annotated[
    RoundingMethod,
    typer.Option(
        "--taxes-rounding-method",
        envvar="TAXES_TAXES_ROUNDING_METHOD",
        rich_help_panel="Taxes Rounding",
    ),
]
TaxesRoundToNearestOpt = Annotated[
    float,
    typer.Option(
        "--taxes-round-to-nearest",
        envvar="TAXES_TAXES_ROUND_TO_NEAREST",
        rich_help_panel="Taxes Rounding",
    ),
]


MinAllowedSalaryOpt = Annotated[
    float,
    typer.Option(
        "--min-allowed-salary",
        envvar="TAXES_MIN_ALLOWED_SALARY",
    ),
]
FixedTaxRateOpt = Annotated[
    float,
    typer.Option(
        "--fixed-tax-rate",
        envvar="TAXES_FIXED_TAX_RATE",
    ),
]

WritePathOpt = Annotated[
    Path | None,
    typer.Option(
        "-e",
        "--write-path",
        help="Path to the output file",
        exists=False,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        callback=write_path_callback,
    ),
]


GrossSalaryArg = Annotated[float, typer.Argument()]
GrossCompensationsArg = Annotated[float, typer.Argument()]
SocialSecuritySalaryOpt = Annotated[float | None, typer.Argument(callback=ss_salary_callback)]

TargetSalaryArg = Annotated[float, typer.Argument()]


SsRoundingMethodOpt = Annotated[
    RoundingMethod,
    typer.Option(
        "--ss-rounding-method",
        envvar="TAXES_SS_ROUNDING_METHOD",
        rich_help_panel="Social Security",
    ),
]

SsRoundToNearestOpt = Annotated[
    float,
    typer.Option(
        "--ss-round-to-nearest",
        envvar="TAXES_SS_ROUND_TO_NEAREST",
        rich_help_panel="Social Security",
    ),
]

MinSsAllowedSalaryOpt = Annotated[
    float,
    typer.Option(
        "--min-ss-allowed-salary",
        envvar="TAXES_MIN_SS_ALLOWED_SALARY",
        rich_help_panel="Social Security",
    ),
]

SsDeductionRateOpt = Annotated[
    float,
    typer.Option(
        "--ss-deduction-rate",
        envvar="TAXES_SS_DEDUCTION_RATE",
        rich_help_panel="Social Security",
    ),
]
