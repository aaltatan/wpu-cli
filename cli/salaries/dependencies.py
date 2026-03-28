# ruff: noqa: B008
from decimal import Decimal

import xlwings as xw
from syriantaxes import Rounder, RoundingMethod, SocialSecurity
from typer_di import Depends

from .loaders.row import RowLoader
from .loaders.settings import load_settings as _load_settings
from .models import SalaryInSchema, SettingsSchema
from .options import (
    CalculationRoundingMethodOpt,
    CalculationRoundToNearestOpt,
    SalariesFilePasswordOpt,
    SalariesFilePathArg,
    SSRoundingMethodOpt,
    SSRoundToNearestOpt,
    TaxesRoundingMethodOpt,
    TaxesRoundToNearestOpt,
)

DATA_SHEET_NAME = "Data"
DATA_TABLE_NAME = "Data"
SETTINGS_SHEET_NAME = "STS"


def _get_ss_rounder(
    ss_round_to_nearest: SSRoundToNearestOpt = Decimal(1),
    ss_rounding_method: SSRoundingMethodOpt = RoundingMethod.HALF_UP,
) -> Rounder:
    return Rounder(method=ss_rounding_method, to_nearest=ss_round_to_nearest)


def _load_salaries_book(path: SalariesFilePathArg, password: SalariesFilePasswordOpt) -> xw.Book:
    return xw.Book(path, password=password)


def _load_data_sheet(book: xw.Book = Depends(_load_salaries_book)) -> xw.Sheet:
    return book.sheets[DATA_SHEET_NAME]


def _load_settings_sheet(book: xw.Book = Depends(_load_salaries_book)) -> xw.Sheet:
    return book.sheets[SETTINGS_SHEET_NAME]


def load_settings(ws: xw.Sheet = Depends(_load_settings_sheet)) -> SettingsSchema:
    return _load_settings(ws)


def load_rows(
    ws: xw.Sheet = Depends(_load_data_sheet),
    settings: SettingsSchema = Depends(load_settings),
) -> list[SalaryInSchema]:
    rg = ws.range(DATA_TABLE_NAME)

    if rg.value is None and not isinstance(rg.value, list):
        message = f"Range value is not a list: {rg.value}"
        raise TypeError(message)

    return [RowLoader(row, settings.fixed_tax_columns).load() for row in rg.value]


def get_calculation_rounder(
    calc_round_to_nearest: CalculationRoundToNearestOpt = Decimal(1),
    calc_rounding_method: CalculationRoundingMethodOpt = RoundingMethod.HALF_UP,
) -> Rounder:
    return Rounder(method=calc_rounding_method, to_nearest=calc_round_to_nearest)


def get_taxes_rounder(
    tax_round_to_nearest: TaxesRoundToNearestOpt = Decimal(100),
    tax_rounding_method: TaxesRoundingMethodOpt = RoundingMethod.HALF_UP,
) -> Rounder:
    return Rounder(method=tax_rounding_method, to_nearest=tax_round_to_nearest)


def get_ss_obj(
    settings: SettingsSchema = Depends(load_settings),
    rounder: Rounder = Depends(_get_ss_rounder),
) -> SocialSecurity:
    return SocialSecurity(
        min_salary=settings.min_ss_salary,
        deduction_rate=settings.ss_deduction_rate,
        rounder=rounder,
    )
