# ruff: noqa: B008
from decimal import Decimal

import xlwings as xw
from syriantaxes import Rounder, RoundingMethod, SocialSecurity
from typer_di import Depends

from .loaders.row import RowLoader
from .loaders.settings import SettingsLoader
from .models import SalaryInSchema, SettingsSchema
from .options import (
    CalculationRoundingMethodOpt,
    CalculationRoundToNearestOpt,
    SalariesFilePasswordOpt,
    SalariesFilePathArg,
    SSRoundingMethodOpt,
    SSRoundToNearestOpt,
    StartRowOpt,
    TaxesRoundingMethodOpt,
    TaxesRoundToNearestOpt,
)


def _get_ss_rounder(
    round_to_nearest: SSRoundToNearestOpt = Decimal(1),
    rounding_method: SSRoundingMethodOpt = RoundingMethod.HALF_UP,
) -> Rounder:
    return Rounder(method=rounding_method, to_nearest=round_to_nearest)


def _load_salaries_book(path: SalariesFilePathArg, password: SalariesFilePasswordOpt) -> xw.Book:
    return xw.Book(path, password=password)


def _load_last_row(book: xw.Book = Depends(_load_salaries_book)) -> int:
    # TODO: implement
    return 10


def load_settings(book: xw.Book = Depends(_load_salaries_book)) -> SettingsSchema:
    return SettingsLoader(book).load()


def load_rows(
    book: xw.Book = Depends(_load_salaries_book),
    settings: SettingsSchema = Depends(load_settings),
    start_row: StartRowOpt = 3,
    last_row: int = Depends(_load_last_row),
) -> list[SalaryInSchema]:
    return [
        RowLoader(book, idx, settings.fixed_tax_columns).load()
        for idx in range(start_row, last_row + 1)
    ]


def get_calculation_rounder(
    round_to_nearest: CalculationRoundToNearestOpt = Decimal(1),
    rounding_method: CalculationRoundingMethodOpt = RoundingMethod.HALF_UP,
) -> Rounder:
    return Rounder(method=rounding_method, to_nearest=round_to_nearest)


def get_taxes_rounder(
    round_to_nearest: TaxesRoundToNearestOpt = Decimal(100),
    rounding_method: TaxesRoundingMethodOpt = RoundingMethod.HALF_UP,
) -> Rounder:
    return Rounder(method=rounding_method, to_nearest=round_to_nearest)


def get_ss_obj(
    settings: SettingsSchema = Depends(load_settings),
    rounder: Rounder = Depends(_get_ss_rounder),
) -> SocialSecurity:
    return SocialSecurity(
        min_salary=settings.min_ss_salary,
        deduction_rate=settings.ss_deduction_rate,
        rounder=rounder,
    )
