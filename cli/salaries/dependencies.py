# ruff: noqa: B008
from collections.abc import Callable
from decimal import Decimal

import xlwings as xw
from syriantaxes import Rounder, RoundingMethod, SocialSecurity
from typer_di import Depends

from .models import RowSchema, SettingsSchema
from .options import (
    CalculatedEndColumnOpt,
    CalculatedStartColumnOpt,
    CalculationRoundingMethodOpt,
    CalculationRoundToNearestOpt,
    SalariesWorkbookPasswordOpt,
    SalariesWorkbookPathArg,
    SSRoundingMethodOpt,
    SSRoundToNearestOpt,
    StartRowOpt,
    TaxesRoundingMethodOpt,
    TaxesRoundToNearestOpt,
    WriteConfirmationOpt,
)
from .readers.row import RowReader
from .readers.settings import read_settings
from .services import SalaryCalculator

type Array[T] = list[list[T]]
type WriterFn = Callable[[Array[float]], xw.Sheet]

DATA_SHEET_NAME = "Data"
DATA_TABLE_NAME = "Data"
SETTINGS_SHEET_NAME = "STS"

CALCULATED_START_COLUMN = "AW"
CALCULATED_END_COLUMN = "CW"
START_ROW = 3


def _get_salaries_workbook(
    path: SalariesWorkbookPathArg, password: SalariesWorkbookPasswordOpt
) -> xw.Book:
    return xw.Book(path, password=password)


def _get_data_worksheet(wb: xw.Book = Depends(_get_salaries_workbook)) -> xw.Sheet:
    return wb.sheets[DATA_SHEET_NAME]


def _read_settings(wb: xw.Book = Depends(_get_salaries_workbook)) -> SettingsSchema:
    return read_settings(wb.sheets[SETTINGS_SHEET_NAME])


def _read_raw_data(
    ws: xw.Sheet = Depends(_get_data_worksheet),
    settings: SettingsSchema = Depends(_read_settings),
) -> list[RowSchema]:
    rg = ws.range(DATA_TABLE_NAME)

    if rg.value is None and not isinstance(rg.value, list):
        message = f"Range value is not a list: {rg.value}"
        raise TypeError(message)

    return [RowReader(row, settings.fixed_tax_columns).read() for row in rg.value]


def _get_ss_rounder(
    ss_round_to_nearest: SSRoundToNearestOpt = Decimal(1),
    ss_rounding_method: SSRoundingMethodOpt = RoundingMethod.HALF_UP,
) -> Rounder:
    return Rounder(ss_rounding_method, ss_round_to_nearest)


def _get_taxes_rounder(
    tax_round_to_nearest: TaxesRoundToNearestOpt = Decimal(100),
    tax_rounding_method: TaxesRoundingMethodOpt = RoundingMethod.HALF_UP,
) -> Rounder:
    return Rounder(tax_rounding_method, tax_round_to_nearest)


def _get_calculation_rounder(
    calc_round_to_nearest: CalculationRoundToNearestOpt = Decimal(1),
    calc_rounding_method: CalculationRoundingMethodOpt = RoundingMethod.HALF_UP,
) -> Rounder:
    return Rounder(calc_rounding_method, calc_round_to_nearest)


def _get_ss_obj(
    settings: SettingsSchema = Depends(_read_settings),
    rounder: Rounder = Depends(_get_ss_rounder),
) -> SocialSecurity:
    return SocialSecurity(settings.min_ss_salary, settings.ss_deduction_rate, rounder)


def get_calculated_array(
    rows: list[RowSchema] = Depends(_read_raw_data),
    settings: SettingsSchema = Depends(_read_settings),
    calculation_rounder: Rounder = Depends(_get_calculation_rounder),
    tax_rounder: Rounder = Depends(_get_taxes_rounder),
    ss_obj: SocialSecurity = Depends(_get_ss_obj),
) -> Array[float]:
    return [
        SalaryCalculator(row, settings, calculation_rounder, tax_rounder, ss_obj)
        .calculate()
        .as_row()
        for row in rows
    ]


def get_writer_fn(
    ws: xw.Sheet = Depends(_get_data_worksheet),
    start_col: CalculatedStartColumnOpt = CALCULATED_START_COLUMN,
    end_col: CalculatedEndColumnOpt = CALCULATED_END_COLUMN,
    start_row: StartRowOpt = START_ROW,
    write: WriteConfirmationOpt = False,  # noqa: FBT002
) -> WriterFn | None:
    def wrapper(data: Array[float]) -> xw.Sheet:
        ws.range(f"{start_col}{start_row}:{end_col}{len(data)}").options(index=False).value = data
        return ws

    if write:
        return wrapper

    return None
