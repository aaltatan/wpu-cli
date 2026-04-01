from decimal import Decimal

import xlwings as xw

from cli.salaries.enums import SettingCell
from cli.salaries.mappers import BRACKETS_RANGE, FIXED_TAX_COLUMNS_RANGE, SETTINGS_CELLS_MAPPER
from cli.salaries.models import BracketSchema, SettingsSchema
from cli.salaries.utils import generate_column_idx


class SettingNotInitializedError(Exception):
    def __init__(self, setting: SettingCell, *args: object) -> None:
        message = f"Setting {setting} is not initialized"
        super().__init__(message, *args)


def read_settings(ws: xw.Sheet) -> SettingsSchema:
    frc = Decimal("0.01")

    fixed_tax_rate = _read_cell(ws, SettingCell.FIXED_TAX_RATE).quantize(frc)
    ss_deduction_rate = _read_cell(ws, SettingCell.SS_DEDUCTION_RATE).quantize(frc)
    tu_monthly_deduction_rate = _read_cell(ws, SettingCell.TU_MONTHLY_DEDUCTION_RATE).quantize(frc)
    tu_pension_deduction_rate = _read_cell(ws, SettingCell.TU_PENSION_DEDUCTION_RATE).quantize(frc)
    healthy_leaves_rate = _read_cell(ws, SettingCell.HEALTHY_LEAVES_RATE).quantize(frc)
    healthy_leaves_based_on = _read_cell(ws, SettingCell.HEALTHY_LEAVES_BASED_ON, str)
    days_of_month = _read_cell(ws, SettingCell.DAYS_OF_MONTH).quantize(frc)
    leaves_without_pay_rate = _read_cell(ws, SettingCell.LEAVES_WITHOUT_PAY_RATE)
    leaves_without_pay_based_on = _read_cell(ws, SettingCell.LEAVES_WITHOUT_PAY_BASED_ON, str)
    overtime_rate = _read_cell(ws, SettingCell.OVERTIME_RATE).quantize(frc)
    overtime_based_on = _read_cell(ws, SettingCell.OVERTIME_BASED_ON, str)
    additional_leaves_rate = _read_cell(ws, SettingCell.ADDITIONAL_LEAVES_RATE).quantize(frc)
    additional_leaves_based_on = _read_cell(ws, SettingCell.ADDITIONAL_LEAVES_BASED_ON, str)
    min_ss_salary = _read_cell(ws, SettingCell.MIN_SS_SALARY).quantize(frc)
    min_allowed_salary = _read_cell(ws, SettingCell.MIN_ALLOWED_SALARY).quantize(frc)

    fixed_tax_columns = _read_fixed_tax_columns(ws)
    brackets = _read_brackets(ws)

    return SettingsSchema(
        fixed_tax_rate=fixed_tax_rate,
        ss_deduction_rate=ss_deduction_rate,
        tu_monthly_deduction_rate=tu_monthly_deduction_rate,
        tu_pension_deduction_rate=tu_pension_deduction_rate,
        healthy_leaves_rate=healthy_leaves_rate,
        healthy_leaves_based_on=healthy_leaves_based_on,  # type: ignore  # noqa: PGH003
        days_of_month=days_of_month,
        leaves_without_pay_rate=leaves_without_pay_rate,
        leaves_without_pay_based_on=leaves_without_pay_based_on,  # type: ignore  # noqa: PGH003
        overtime_rate=overtime_rate,
        overtime_based_on=overtime_based_on,  # type: ignore  # noqa: PGH003
        additional_leaves_rate=additional_leaves_rate,
        additional_leaves_based_on=additional_leaves_based_on,  # type: ignore  # noqa: PGH003
        fixed_tax_columns=fixed_tax_columns,
        brackets=brackets,
        min_ss_salary=min_ss_salary,
        min_allowed_salary=min_allowed_salary,
    )


def _read_brackets(ws: xw.Sheet) -> list[BracketSchema]:
    rg = ws.range(BRACKETS_RANGE)

    brackets: list[BracketSchema] = []

    if not isinstance(rg.value, list):
        message = f"Brackets range value is not a list: {rg.value}"
        raise TypeError(message)

    for row in rg.value:
        _min, _max, rate = row

        if not isinstance(_min, float):
            message = f"Bracket min is not a float: {_min}"
            raise TypeError(message)

        if not isinstance(_max, float):
            message = f"Bracket max is not a float: {_max}"
            raise TypeError(message)

        if not isinstance(rate, float):
            message = f"Bracket rate is not a float: {rate}"
            raise TypeError(message)

        brackets.append(
            BracketSchema(
                min=Decimal(_min).quantize(Decimal(1)),
                max=Decimal(_max).quantize(Decimal(1)),
                rate=Decimal(rate).quantize(Decimal("0.01")),
            )
        )

    return brackets


def _read_fixed_tax_columns(ws: xw.Sheet) -> list[int]:
    rg = ws.range(FIXED_TAX_COLUMNS_RANGE)
    # 5 is the first column index
    return [generate_column_idx(str(cell.value)) - 5 for cell in rg if cell.value is not None]


def _read_cell[T: (Decimal, str)](ws: xw.Sheet, setting: SettingCell, cast: type[T] = Decimal) -> T:
    value = ws.range(SETTINGS_CELLS_MAPPER[setting]).value

    if value is None:
        raise SettingNotInitializedError(setting)

    return cast(value)
