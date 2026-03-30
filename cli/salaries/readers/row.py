from decimal import Decimal
from typing import Any

from cli.salaries.enums import RawColumn
from cli.salaries.mappers import RAW_COLUMNS_MAPPER
from cli.salaries.models import CompensationSchema, SalaryInSchema


class RowReader:
    def __init__(self, row: list[Any], fixed_tax_columns: list[int]) -> None:
        self._row = row
        self._fixed_tax_columns = fixed_tax_columns

    def read(self) -> SalaryInSchema:
        days_of_work_count = self._get_cell_value(RawColumn.DAYS_OF_WORK_COUNT)
        overtime_days_count = self._get_cell_value(RawColumn.OVERTIME_DAYS_COUNT)
        healthy_leaves_count = self._get_cell_value(RawColumn.HEALTHY_LEAVES_COUNT)
        without_pay_leaves_count = self._get_cell_value(RawColumn.WITHOUT_PAY_LEAVES_COUNT)
        additional_leaves_count = self._get_cell_value(RawColumn.ADDITIONAL_LEAVES_COUNT)

        hours_count = self._get_cell_value(RawColumn.HOURS_COUNT)
        hour_price = self._get_cell_value(RawColumn.HOUR_PRICE)

        fixed_salary = self._get_cell_value(RawColumn.FIXED_SALARY)

        compensation_01 = self._get_compensation(RawColumn.COMPENSATION_01)
        compensation_02 = self._get_compensation(RawColumn.COMPENSATION_02)
        compensation_03 = self._get_compensation(RawColumn.COMPENSATION_03)
        compensation_04 = self._get_compensation(RawColumn.COMPENSATION_04)
        compensation_05 = self._get_compensation(RawColumn.COMPENSATION_05)
        compensation_06 = self._get_compensation(RawColumn.COMPENSATION_06)
        compensation_07 = self._get_compensation(RawColumn.COMPENSATION_07)
        compensation_08 = self._get_compensation(RawColumn.COMPENSATION_08)
        compensation_09 = self._get_compensation(RawColumn.COMPENSATION_09)
        compensation_10 = self._get_compensation(RawColumn.COMPENSATION_10)
        compensation_11 = self._get_compensation(RawColumn.COMPENSATION_11)
        compensation_12 = self._get_compensation(RawColumn.COMPENSATION_12)
        compensation_13 = self._get_compensation(RawColumn.COMPENSATION_13)
        compensation_14 = self._get_compensation(RawColumn.COMPENSATION_14)
        compensation_15 = self._get_compensation(RawColumn.COMPENSATION_15)

        additional_compensation_01 = self._get_compensation(RawColumn.ADDITIONAL_COMPENSATION_01)
        additional_compensation_02 = self._get_compensation(RawColumn.ADDITIONAL_COMPENSATION_02)
        additional_compensation_03 = self._get_compensation(RawColumn.ADDITIONAL_COMPENSATION_03)
        additional_compensation_04 = self._get_compensation(RawColumn.ADDITIONAL_COMPENSATION_04)
        additional_compensation_05 = self._get_compensation(RawColumn.ADDITIONAL_COMPENSATION_05)
        additional_compensation_06 = self._get_compensation(RawColumn.ADDITIONAL_COMPENSATION_06)
        additional_compensation_07 = self._get_compensation(RawColumn.ADDITIONAL_COMPENSATION_07)
        additional_compensation_08 = self._get_compensation(RawColumn.ADDITIONAL_COMPENSATION_08)
        additional_compensation_09 = self._get_compensation(RawColumn.ADDITIONAL_COMPENSATION_09)
        additional_compensation_10 = self._get_compensation(RawColumn.ADDITIONAL_COMPENSATION_10)

        deduction_01 = self._get_compensation(RawColumn.DEDUCTION_01)
        deduction_02 = self._get_compensation(RawColumn.DEDUCTION_02)

        deduction_03 = self._get_compensation(RawColumn.DEDUCTION_03)
        deduction_04 = self._get_compensation(RawColumn.DEDUCTION_04)
        deduction_05 = self._get_compensation(RawColumn.DEDUCTION_05)
        deduction_06 = self._get_compensation(RawColumn.DEDUCTION_06)
        deduction_07 = self._get_compensation(RawColumn.DEDUCTION_07)
        deduction_08 = self._get_compensation(RawColumn.DEDUCTION_08)
        deduction_09 = self._get_compensation(RawColumn.DEDUCTION_09)
        deduction_10 = self._get_compensation(RawColumn.DEDUCTION_10)
        deduction_11 = self._get_compensation(RawColumn.DEDUCTION_11)
        deduction_12 = self._get_compensation(RawColumn.DEDUCTION_12)

        ss = self._get_cell_value(RawColumn.SS_SALARY)
        tu = self._get_cell_value(RawColumn.TU_SALARY)

        return SalaryInSchema(
            days_of_work_count=days_of_work_count,
            overtime_days_count=overtime_days_count,
            healthy_leaves_count=healthy_leaves_count,
            without_pay_leaves_count=without_pay_leaves_count,
            additional_leaves_count=additional_leaves_count,
            hours_count=hours_count,
            hour_price=hour_price,
            fixed_salary=fixed_salary,
            compensation_01=compensation_01,
            compensation_02=compensation_02,
            compensation_03=compensation_03,
            compensation_04=compensation_04,
            compensation_05=compensation_05,
            compensation_06=compensation_06,
            compensation_07=compensation_07,
            compensation_08=compensation_08,
            compensation_09=compensation_09,
            compensation_10=compensation_10,
            compensation_11=compensation_11,
            compensation_12=compensation_12,
            compensation_13=compensation_13,
            compensation_14=compensation_14,
            compensation_15=compensation_15,
            additional_compensation_01=additional_compensation_01,
            additional_compensation_02=additional_compensation_02,
            additional_compensation_03=additional_compensation_03,
            additional_compensation_04=additional_compensation_04,
            additional_compensation_05=additional_compensation_05,
            additional_compensation_06=additional_compensation_06,
            additional_compensation_07=additional_compensation_07,
            additional_compensation_08=additional_compensation_08,
            additional_compensation_09=additional_compensation_09,
            additional_compensation_10=additional_compensation_10,
            deduction_01=deduction_01,
            deduction_02=deduction_02,
            deduction_03=deduction_03,
            deduction_04=deduction_04,
            deduction_05=deduction_05,
            deduction_06=deduction_06,
            deduction_07=deduction_07,
            deduction_08=deduction_08,
            deduction_09=deduction_09,
            deduction_10=deduction_10,
            deduction_11=deduction_11,
            deduction_12=deduction_12,
            social_security=ss,
            teachers_union=tu,
        )

    def _get_idx(self, column: RawColumn, *, is_taxable: bool) -> int:
        value = RAW_COLUMNS_MAPPER[column]

        if isinstance(value, int):
            return value

        idx, taxable_idx = value

        if is_taxable:
            return taxable_idx

        return idx

    def _get_compensation(self, column: RawColumn) -> CompensationSchema:
        idx = self._get_idx(column, is_taxable=True)
        value = self._get_cell_value(column)

        return CompensationSchema(value=value, is_taxable=idx in self._fixed_tax_columns)

    def _get_cell_value[T: Decimal](self, column: RawColumn, cast: type[T] = Decimal) -> T:
        value = self._row[self._get_idx(column, is_taxable=False)]

        if value is None:
            value = Decimal(0)

        return cast(value)
