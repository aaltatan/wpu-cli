import typer
from syriantaxes import Bracket, Rounder, SocialSecurity

from .options import (
    BracketMaxesOption,
    BracketMinsOption,
    BracketRatesOption,
    FixedTaxRateOption,
    MinAllowedSalaryOption,
    MinSsAllowedSalaryOption,
    SsDeductionRateOption,
    SsRoundingMethodOption,
    SsRoundToNearestOption,
    TaxesRoundingMethodOption,
    TaxesRoundToNearestOption,
)


def _get_brackets(
    mins: list[float], maxes: list[float], rates: list[float]
) -> list[Bracket]:
    return [
        Bracket(_min, _max, rate)
        for _min, _max, rate in zip(mins, maxes, rates, strict=True)
    ]


def app_callback(  # noqa: PLR0913
    ctx: typer.Context,
    brackets_mins: BracketMinsOption,
    brackets_maxes: BracketMaxesOption,
    brackets_rates: BracketRatesOption,
    min_allowed_salary: MinAllowedSalaryOption,
    taxes_rounding_method: TaxesRoundingMethodOption,
    taxes_round_to_nearest: TaxesRoundToNearestOption,
    ss_rounding_method: SsRoundingMethodOption,
    ss_round_to_nearest: SsRoundToNearestOption,
    min_ss_allowed_salary: MinSsAllowedSalaryOption,
    ss_deduction_rate: SsDeductionRateOption,
    fixed_tax_rate: FixedTaxRateOption,
):
    """Calculate taxes based on Syrian taxes rules."""
    brackets = _get_brackets(brackets_mins, brackets_maxes, brackets_rates)
    tax_rounder = Rounder(taxes_rounding_method, taxes_round_to_nearest)
    ss_rounder = Rounder(ss_rounding_method, ss_round_to_nearest)
    ss = SocialSecurity(
        min_ss_allowed_salary, ss_deduction_rate, rounder=ss_rounder
    )

    ctx.obj = {
        "brackets": brackets,
        "min_allowed_salary": min_allowed_salary,
        "tax_rounder": tax_rounder,
        "fixed_tax_rate": fixed_tax_rate,
        "ss": ss,
    }
