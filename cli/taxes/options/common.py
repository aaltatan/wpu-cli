from dataclasses import InitVar, dataclass, field
from typing import Annotated

import typer
from syriantaxes import Bracket, Rounder, RoundingMethod

BracketMinsOption = Annotated[
    list[float],
    typer.Option(
        "--brackets-mins",
        default_factory=list,
        envvar="TAXES_BRACKET_TAX_MINS",
        rich_help_panel="Brackets",
    ),
]

BracketMaxesOption = Annotated[
    list[float],
    typer.Option(
        "--brackets-maxs",
        default_factory=list,
        envvar="TAXES_BRACKET_TAX_MAXS",
        rich_help_panel="Brackets",
    ),
]

BracketRatesOption = Annotated[
    list[float],
    typer.Option(
        "--brackets-rates",
        default_factory=list,
        envvar="TAXES_BRACKET_TAX_RATES",
        rich_help_panel="Brackets",
    ),
]

MinAllowedSalaryOption = Annotated[
    float,
    typer.Option(
        "--min-allowed-salary",
        envvar="TAXES_MIN_ALLOWED_SALARY",
    ),
]

FixedTaxRateOption = Annotated[
    float,
    typer.Option(
        "--fixed-tax-rate",
        envvar="TAXES_FIXED_TAX_RATE",
    ),
]

TaxesRoundingMethodOption = Annotated[
    RoundingMethod,
    typer.Option(
        "--taxes-rounding-method",
        envvar="TAXES_TAXES_ROUNDING_METHOD",
        rich_help_panel="Taxes Rounding",
    ),
]

TaxesRoundToNearestOption = Annotated[
    float,
    typer.Option(
        "--taxes-round-to-nearest",
        envvar="TAXES_TAXES_ROUND_TO_NEAREST",
        rich_help_panel="Taxes Rounding",
    ),
]


def _get_brackets(
    mins: BracketMinsOption, maxes: BracketMaxesOption, rates: BracketRatesOption
) -> list[Bracket]:
    return [Bracket(mins, maxs, rate) for mins, maxs, rate in zip(mins, maxes, rates, strict=True)]


def _get_rounder(
    taxes_rounding_method: RoundingMethod, taxes_rounding_to_nearest: float
) -> Rounder:
    return Rounder(taxes_rounding_method, taxes_rounding_to_nearest)


@dataclass
class Options:
    brackets_mins: InitVar[BracketMinsOption]
    brackets_maxs: InitVar[BracketMaxesOption]
    brackets_rates: InitVar[BracketRatesOption]

    taxes_rounding_method: InitVar[TaxesRoundingMethodOption]
    taxes_rounding_to_nearest: InitVar[TaxesRoundToNearestOption]

    min_allowed_salary: MinAllowedSalaryOption
    fixed_tax_rate: FixedTaxRateOption

    brackets: list[Bracket] = field(init=False)
    taxes_rounder: Rounder = field(init=False)

    def __post_init__(
        self,
        brackets_mins: BracketMinsOption,
        brackets_maxs: BracketMaxesOption,
        brackets_rates: BracketRatesOption,
        taxes_rounding_method: TaxesRoundingMethodOption,
        taxes_rounding_to_nearest: TaxesRoundToNearestOption,
    ) -> None:
        self.brackets = _get_brackets(brackets_mins, brackets_maxs, brackets_rates)
        self.taxes_rounder = _get_rounder(taxes_rounding_method, taxes_rounding_to_nearest)


def get_options(  # noqa: PLR0913
    brackets_mins: BracketMinsOption,
    brackets_maxs: BracketMaxesOption,
    brackets_rates: BracketRatesOption,
    taxes_rounding_method: TaxesRoundingMethodOption,
    taxes_rounding_to_nearest: TaxesRoundToNearestOption,
    min_allowed_salary: MinAllowedSalaryOption,
    fixed_tax_rate: FixedTaxRateOption,
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
