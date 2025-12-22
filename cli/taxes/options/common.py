from dataclasses import InitVar, dataclass, field
from typing import Annotated

import typer
from syriantaxes import Bracket, Rounder, RoundingMethod

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


def _get_brackets(
    mins: BracketMinsOpt, maxes: BracketMaxesOpt, rates: BracketRatesOpt
) -> list[Bracket]:
    return [Bracket(mins, maxs, rate) for mins, maxs, rate in zip(mins, maxes, rates, strict=True)]


def _get_rounder(
    taxes_rounding_method: RoundingMethod, taxes_rounding_to_nearest: float
) -> Rounder:
    return Rounder(taxes_rounding_method, taxes_rounding_to_nearest)


@dataclass
class Options:
    brackets_mins: InitVar[BracketMinsOpt]
    brackets_maxs: InitVar[BracketMaxesOpt]
    brackets_rates: InitVar[BracketRatesOpt]

    taxes_rounding_method: InitVar[TaxesRoundingMethodOpt]
    taxes_rounding_to_nearest: InitVar[TaxesRoundToNearestOpt]

    min_allowed_salary: MinAllowedSalaryOpt
    fixed_tax_rate: FixedTaxRateOpt

    brackets: list[Bracket] = field(init=False)
    taxes_rounder: Rounder = field(init=False)

    def __post_init__(
        self,
        brackets_mins: BracketMinsOpt,
        brackets_maxs: BracketMaxesOpt,
        brackets_rates: BracketRatesOpt,
        taxes_rounding_method: TaxesRoundingMethodOpt,
        taxes_rounding_to_nearest: TaxesRoundToNearestOpt,
    ) -> None:
        self.brackets = _get_brackets(brackets_mins, brackets_maxs, brackets_rates)
        self.taxes_rounder = _get_rounder(taxes_rounding_method, taxes_rounding_to_nearest)


def get_options(  # noqa: PLR0913
    brackets_mins: BracketMinsOpt,
    brackets_maxs: BracketMaxesOpt,
    brackets_rates: BracketRatesOpt,
    taxes_rounding_method: TaxesRoundingMethodOpt,
    taxes_rounding_to_nearest: TaxesRoundToNearestOpt,
    min_allowed_salary: MinAllowedSalaryOpt,
    fixed_tax_rate: FixedTaxRateOpt,
) -> Options:
    return Options(
        brackets_mins,
        brackets_maxs,
        brackets_rates,
        taxes_rounding_method,
        taxes_rounding_to_nearest,
        min_allowed_salary,
        fixed_tax_rate,
    )
