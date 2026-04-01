# ruff: noqa: B008
from decimal import Decimal

import xlwings as xw
from syriantaxes import Rounder, RoundingMethod, SocialSecurity
from typer_di import Depends

from .models import SalaryInSchema, SettingsSchema
from .options import (
    CalculationRoundingMethodOpt,
    CalculationRoundToNearestOpt,
    SalariesWorkbookPasswordOpt,
    SalariesWorkbookPathArg,
    SSRoundingMethodOpt,
    SSRoundToNearestOpt,
    TaxesRoundingMethodOpt,
    TaxesRoundToNearestOpt,
)
from .readers.row import RowReader
from .readers.settings import read_settings as _read_settings

DATA_SHEET_NAME = "Data"
DATA_TABLE_NAME = "Data"
SETTINGS_SHEET_NAME = "STS"


def _get_ss_rounder(
    ss_round_to_nearest: SSRoundToNearestOpt = Decimal(1),
    ss_rounding_method: SSRoundingMethodOpt = RoundingMethod.HALF_UP,
) -> Rounder:
    return Rounder(method=ss_rounding_method, to_nearest=ss_round_to_nearest)


def _get_salaries_workbook(
    path: SalariesWorkbookPathArg, password: SalariesWorkbookPasswordOpt
) -> xw.Book:
    return xw.Book(path, password=password)


def get_data_worksheet(book: xw.Book = Depends(_get_salaries_workbook)) -> xw.Sheet:
    return book.sheets[DATA_SHEET_NAME]


def _get_settings_worksheet(book: xw.Book = Depends(_get_salaries_workbook)) -> xw.Sheet:
    return book.sheets[SETTINGS_SHEET_NAME]


def read_settings(ws: xw.Sheet = Depends(_get_settings_worksheet)) -> SettingsSchema:
    return _read_settings(ws)


def read_rows(
    ws: xw.Sheet = Depends(get_data_worksheet),
    settings: SettingsSchema = Depends(read_settings),
) -> list[SalaryInSchema]:
    rg = ws.range(DATA_TABLE_NAME)

    if rg.value is None and not isinstance(rg.value, list):
        message = f"Range value is not a list: {rg.value}"
        raise TypeError(message)

    return [RowReader(row, settings.fixed_tax_columns).read() for row in rg.value]


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
    settings: SettingsSchema = Depends(read_settings),
    rounder: Rounder = Depends(_get_ss_rounder),
) -> SocialSecurity:
    return SocialSecurity(
        min_salary=settings.min_ss_salary,
        deduction_rate=settings.ss_deduction_rate,
        rounder=rounder,
    )
