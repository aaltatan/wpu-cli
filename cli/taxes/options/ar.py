import os
from dataclasses import dataclass
from typing import Annotated

import typer

from ._options import CompensationsRateOpt, WritePathOpt

FACTOR = 10
MAX_ITERATIONS = 1000


def amount_range_start_callback(value: float) -> float:
    min_salary = int(os.getenv("TAXES_MIN_ALLOWED_SALARY", default="0"))
    if value < min_salary:
        message = f"The start value must be greater than {min_salary}."
        raise typer.BadParameter(message)

    return value


StartAmountRangeArg = Annotated[
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


StopAmountRangeArg = Annotated[
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


StepAmountRangeArg = Annotated[
    float | None,
    typer.Argument(
        callback=amount_range_step_callback,
    ),
]


@dataclass
class AmountRangeOption:
    start: StartAmountRangeArg
    compensations_rate: CompensationsRateOpt
    stop: StopAmountRangeArg = None
    step: StepAmountRangeArg = None
    write_path: WritePathOpt = None
