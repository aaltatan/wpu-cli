import os
from pathlib import Path

import typer

from cli.utils import extract_extension

FACTOR = 10
MAX_ITERATIONS = 1000


def amount_range_start_callback(value: float) -> float:
    min_salary = int(os.getenv("TAXES_MIN_ALLOWED_SALARY", default="0"))
    if value < min_salary:
        message = f"The start value must be greater than {min_salary}."
        raise typer.BadParameter(message)

    return value


def amount_range_stop_callback(
    ctx: typer.Context, _: typer.CallbackParam, value: float | None
) -> float | None:
    if value is None:
        value = ctx.params["start"] * FACTOR

    if value <= ctx.params["start"]:
        message = "The stop value must be greater than the start value."
        raise typer.BadParameter(message)

    return value


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


def write_path_callback(
    ctx: typer.Context, _: typer.CallbackParam, value: Path | None
) -> Path | None:
    if value:
        if value.exists():
            message = f"The file {value} already exists."
            raise typer.BadParameter(message)

        extension = extract_extension(value)

        if extension not in ctx.obj["registry"]:
            message = f"extension of type ({extension}) not supported."
            raise typer.BadParameter(message)

    return value


def ss_salary_callback(value: float | None) -> float | None:
    if value:
        min_ss_allowed_salary = int(os.getenv("TAXES_MIN_SS_ALLOWED_SALARY", "0"))
        if value < min_ss_allowed_salary:
            message = f"The social security salary must be greater than {min_ss_allowed_salary}."
            raise typer.BadParameter(message)

    return value
