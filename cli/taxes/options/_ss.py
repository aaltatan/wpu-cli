from typing import Annotated

import typer
from syriantaxes import Rounder, RoundingMethod, SocialSecurity
from typer_di import Depends

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


def get_ss_rounder(
    ss_rounding_method: SsRoundingMethodOpt, ss_rounding_to_nearest: SsRoundToNearestOpt
) -> Rounder:
    return Rounder(ss_rounding_method, ss_rounding_to_nearest)


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


def get_ss_obj(
    min_salary: MinSsAllowedSalaryOpt,
    deduction_rate: SsDeductionRateOpt,
    rounder: Rounder = Depends(get_ss_rounder),  # noqa: B008
) -> SocialSecurity:
    return SocialSecurity(min_salary, deduction_rate, rounder)
