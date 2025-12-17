import os
from pathlib import Path
from typing import Annotated

import typer
from syriantaxes import RoundingMethod

from .exporters import get_export_functions, get_extension

FACTOR = 10
MAX_ITERATIONS = 1000

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


def ss_salary_callback(value: float | None) -> float | None:
    if value:
        min_ss_allowed_salary = int(
            os.getenv("TAXES_MIN_SS_ALLOWED_SALARY", "0")
        )
        if value < min_ss_allowed_salary:
            message = f"The social security salary must be greater than {min_ss_allowed_salary}."  # noqa: E501
            raise typer.BadParameter(message)

    return value


SocialSecuritySalaryOption = Annotated[
    float | None,
    typer.Option(
        "-s",
        "--ss",
        "--social-security-salary",
        callback=ss_salary_callback,
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

GrossCompensationsArgument = Annotated[float, typer.Argument()]

TargetSalaryArgument = Annotated[float, typer.Argument()]

CompensationsRateOption = Annotated[
    float,
    typer.Option(
        "-r",
        "--compensations-rate",
        envvar="TAXES_DEFAULT_COMPENSATIONS_RATE",
    ),
]


def amount_range_start_callback(
    _: typer.Context, __: typer.CallbackParam, value: float
) -> float:
    min_salary = int(os.getenv("TAXES_MIN_ALLOWED_SALARY", default="0"))
    if value < min_salary:
        message = f"The start value must be greater than {min_salary}."
        raise typer.BadParameter(message)

    return value


StartAmountRangeArgument = Annotated[
    float,
    typer.Argument(
        callback=amount_range_start_callback,
    ),
]


def amount_range_stop_callback(
    ctx: typer.Context, _: typer.CallbackParam, value: float | None
) -> float | None:
    if value is None:
        value = ctx.params["start"] * FACTOR

    if value <= ctx.params["start"]:
        message = "The stop value must be greater than the start value."
        raise typer.BadParameter(message)

    return value


StopAmountRangeArgument = Annotated[
    float | None,
    typer.Argument(
        callback=amount_range_stop_callback,
    ),
]


def amount_range_step_callback(
    ctx: typer.Context, _: typer.CallbackParam, value: float | None
) -> float | None:
    if value is None:
        value = ctx.params["start"] / FACTOR

    iterations_count = (ctx.params["stop"] - ctx.params["start"]) / value

    if iterations_count < 1:
        message = "The step value must be greater than the stop value."
        raise typer.BadParameter(message)

    if iterations_count > MAX_ITERATIONS:
        message = f"The step value must be less than {MAX_ITERATIONS}."
        raise typer.BadParameter(message)

    if ctx.params["start"] + value > ctx.params["stop"]:
        message = "The step value must be less than the stop value."
        raise typer.BadParameter(message)

    return value


StepAmountRangeArgument = Annotated[
    float | None,
    typer.Argument(
        callback=amount_range_step_callback,
    ),
]


def export_path_callback(value: Path | None) -> Path | None:
    if value:
        if value.exists():
            message = f"The file {value} already exists."
            raise typer.BadParameter(message)

        extension = get_extension(value)

        if extension not in get_export_functions():
            message = f"extension of type (.{extension}) not supported."
            raise typer.BadParameter(message)

    return value


ExportPathOption = Annotated[
    Path | None,
    typer.Option(
        "-e",
        "--export-path",
        help="Path to the output file",
        exists=False,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        callback=export_path_callback,
    ),
]
