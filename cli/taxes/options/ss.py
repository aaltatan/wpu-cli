import os
from typing import Annotated

import typer
from syriantaxes import Rounder, RoundingMethod, SocialSecurity

SsRoundingMethodOption = Annotated[
    RoundingMethod,
    typer.Option(
        "--ss-rounding-method",
        envvar="TAXES_SS_ROUNDING_METHOD",
        rich_help_panel="Social Security",
    ),
]

SsRoundToNearestOption = Annotated[
    float,
    typer.Option(
        "--ss-round-to-nearest",
        envvar="TAXES_SS_ROUND_TO_NEAREST",
        rich_help_panel="Social Security",
    ),
]

MinSsAllowedSalaryOption = Annotated[
    float,
    typer.Option(
        "--min-ss-allowed-salary",
        envvar="TAXES_MIN_SS_ALLOWED_SALARY",
        rich_help_panel="Social Security",
    ),
]

SsDeductionRateOption = Annotated[
    float,
    typer.Option(
        "--ss-deduction-rate",
        envvar="TAXES_SS_DEDUCTION_RATE",
        rich_help_panel="Social Security",
    ),
]


def get_ss_rounder(ss_rounding_method: RoundingMethod, ss_rounding_to_nearest: float) -> Rounder:
    return Rounder(ss_rounding_method, ss_rounding_to_nearest)


def get_ss_obj(
    ss_rounding_method: SsRoundingMethodOption,
    ss_rounding_to_nearest: SsRoundToNearestOption,
    min_ss_allowed_salary: MinSsAllowedSalaryOption,
    ss_deduction_rate: SsDeductionRateOption,
) -> SocialSecurity:
    rounder = get_ss_rounder(ss_rounding_method, ss_rounding_to_nearest)
    return SocialSecurity(min_ss_allowed_salary, ss_deduction_rate, rounder)


def ss_salary_callback(value: float | None) -> float | None:
    if value:
        min_ss_allowed_salary = int(os.getenv("TAXES_MIN_SS_ALLOWED_SALARY", "0"))
        if value < min_ss_allowed_salary:
            message = f"The social security salary must be greater than {min_ss_allowed_salary}."
            raise typer.BadParameter(message)

    return value


SocialSecuritySalaryOption = Annotated[
    float | None,
    typer.Argument(
        callback=ss_salary_callback,
    ),
]
