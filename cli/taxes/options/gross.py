import os
from dataclasses import dataclass
from typing import Annotated

import typer

GrossSalaryArg = Annotated[float, typer.Argument()]

GrossCompensationsArg = Annotated[float, typer.Argument()]


def ss_salary_callback(value: float | None) -> float | None:
    if value:
        min_ss_allowed_salary = int(os.getenv("TAXES_MIN_SS_ALLOWED_SALARY", "0"))
        if value < min_ss_allowed_salary:
            message = f"The social security salary must be greater than {min_ss_allowed_salary}."
            raise typer.BadParameter(message)

    return value


SocialSecuritySalaryOpt = Annotated[
    float | None,
    typer.Argument(
        callback=ss_salary_callback,
    ),
]


@dataclass
class Gross:
    salary: GrossSalaryArg
    compensations: GrossCompensationsArg = 0
    ss_salary: SocialSecuritySalaryOpt = None
