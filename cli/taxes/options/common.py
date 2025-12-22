from dataclasses import dataclass
from typing import Annotated

import typer
from syriantaxes import Bracket, Rounder, RoundingMethod
from typer_di import Depends

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


def get_brackets(
    mins: BracketMinsOpt, maxes: BracketMaxesOpt, rates: BracketRatesOpt
) -> list[Bracket]:
    return [Bracket(mins, maxs, rate) for mins, maxs, rate in zip(mins, maxes, rates, strict=True)]


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


def get_rounder(
    taxes_rounding_method: TaxesRoundingMethodOpt, taxes_rounding_to_nearest: TaxesRoundToNearestOpt
) -> Rounder:
    return Rounder(taxes_rounding_method, taxes_rounding_to_nearest)


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


@dataclass
class Options:
    min_allowed_salary: MinAllowedSalaryOpt
    fixed_tax_rate: FixedTaxRateOpt
    brackets: list[Bracket] = Depends(get_brackets)  # noqa: RUF009
    taxes_rounder: Rounder = Depends(get_rounder)  # noqa: RUF009
