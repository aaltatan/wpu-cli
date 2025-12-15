import typer
from syriantaxes import Rounder

from .options import (
    BracketMaxsOption,
    BracketMinsOption,
    BracketRatesOption,
    MinAllowedSalaryOption,
    SsRoundingMethodOption,
    SsRoundToNearestOption,
    TaxesRoundingMethodOption,
    TaxesRoundToNearestOption,
)
from .services import get_brackets


def app_callback(  # noqa: PLR0913
    ctx: typer.Context,
    brackets_mins: BracketMinsOption,
    brackets_maxs: BracketMaxsOption,
    brackets_rates: BracketRatesOption,
    min_allowed_salary: MinAllowedSalaryOption,
    taxes_rounding_method: TaxesRoundingMethodOption,
    taxes_round_to_nearest: TaxesRoundToNearestOption,
    ss_rounding_method: SsRoundingMethodOption,
    ss_round_to_nearest: SsRoundToNearestOption,
):
    """Calculate taxes."""
    brackets = get_brackets(brackets_mins, brackets_maxs, brackets_rates)
    tax_rounder = Rounder(taxes_rounding_method, taxes_round_to_nearest)
    ss_rounder = Rounder(ss_rounding_method, ss_round_to_nearest)

    ctx.obj["brackets"] = brackets
    ctx.obj["min_allowed_salary"] = min_allowed_salary
    ctx.obj["tax_rounder"] = tax_rounder
    ctx.obj["ss_rounder"] = ss_rounder
