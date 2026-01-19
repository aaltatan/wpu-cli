from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from syriantaxes import Bracket, Rounder, RoundingMethod

from cli.taxes.writers import get_write_functions
from cli.utils import extract_extension

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


def get_taxes_rounder(
    method: TaxesRoundingMethodOpt, to_nearest: TaxesRoundToNearestOpt
) -> Rounder:
    return Rounder(method, to_nearest)


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
class Config:
    min_allowed_salary: MinAllowedSalaryOpt
    fixed_tax_rate: FixedTaxRateOpt


def write_path_callback(value: Path | None) -> Path | None:
    if value:
        if value.exists():
            message = f"The file {value} already exists."
            raise typer.BadParameter(message)

        extension = extract_extension(value)

        if extension not in get_write_functions():
            message = f"extension of type (.{extension}) not supported."
            raise typer.BadParameter(message)

    return value


WritePathOpt = Annotated[
    Path | None,
    typer.Option(
        "-e",
        "--write-path",
        help="Path to the output file",
        exists=False,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        callback=write_path_callback,
    ),
]
