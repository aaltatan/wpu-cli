from decimal import Decimal
from typing import Any

from cli.salaries.mappers import COLUMNS_MAPPER
from cli.salaries.models import CompensationSchema, SalaryInSchema


class RowReader:
    def __init__(self, row: list[Any], fixed_tax_columns: list[int]) -> None:
        self._row = row
        self._fixed_tax_columns = fixed_tax_columns

    def read(self) -> SalaryInSchema:
        days_of_work_count = self._get_cell_value("days_of_work_count")
        overtime_days_count = self._get_compensation("overtime_days_count")
        healthy_leaves_count = self._get_compensation("healthy_leaves_count")
        without_pay_leaves_count = self._get_compensation("without_pay_leaves_count")
        additional_leaves_count = self._get_compensation("additional_leaves_count")

        hours_count = self._get_cell_value("hours_count")
        hour_price = self._get_compensation("hour_price")

        fixed_salary = self._get_cell_value("fixed_salary")

        compensation_01 = self._get_compensation("compensation_01")
        compensation_02 = self._get_compensation("compensation_02")
        compensation_03 = self._get_compensation("compensation_03")
        compensation_04 = self._get_compensation("compensation_04")
        compensation_05 = self._get_compensation("compensation_05")
        compensation_06 = self._get_compensation("compensation_06")
        compensation_07 = self._get_compensation("compensation_07")
        compensation_08 = self._get_compensation("compensation_08")
        compensation_09 = self._get_compensation("compensation_09")
        compensation_10 = self._get_compensation("compensation_10")
        compensation_11 = self._get_compensation("compensation_11")
        compensation_12 = self._get_compensation("compensation_12")
        compensation_13 = self._get_compensation("compensation_13")
        compensation_14 = self._get_compensation("compensation_14")
        compensation_15 = self._get_compensation("compensation_15")

        additional_compensation_01 = self._get_compensation("additional_compensation_01")
        additional_compensation_02 = self._get_compensation("additional_compensation_02")
        additional_compensation_03 = self._get_compensation("additional_compensation_03")
        additional_compensation_04 = self._get_compensation("additional_compensation_04")
        additional_compensation_05 = self._get_compensation("additional_compensation_05")
        additional_compensation_06 = self._get_compensation("additional_compensation_06")
        additional_compensation_07 = self._get_compensation("additional_compensation_07")
        additional_compensation_08 = self._get_compensation("additional_compensation_08")
        additional_compensation_09 = self._get_compensation("additional_compensation_09")
        additional_compensation_10 = self._get_compensation("additional_compensation_10")

        deduction_01 = self._get_compensation("deduction_01")
        deduction_02 = self._get_compensation("deduction_02")

        deduction_03 = self._get_compensation("deduction_03")
        deduction_04 = self._get_compensation("deduction_04")
        deduction_05 = self._get_compensation("deduction_05")
        deduction_06 = self._get_compensation("deduction_06")
        deduction_07 = self._get_compensation("deduction_07")
        deduction_08 = self._get_compensation("deduction_08")
        deduction_09 = self._get_compensation("deduction_09")
        deduction_10 = self._get_compensation("deduction_10")
        deduction_11 = self._get_compensation("deduction_11")
        deduction_12 = self._get_compensation("deduction_12")

        ss = self._get_cell_value("ss_salary")
        tu = self._get_cell_value("tu_salary")

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

    def _get_idx(self, column: str, *, calculated: bool) -> int:
        value = COLUMNS_MAPPER[column]

        if isinstance(value, int):
            return value

        if not isinstance(value, tuple):
            message = f"Column {column} value is not a tuple: {value}"
            raise TypeError(message)

        raw_input, calculated_value = value

        if calculated:
            return calculated_value

        return raw_input

    def _get_compensation(self, column: str) -> CompensationSchema:
        idx = self._get_idx(column, calculated=True)
        value = self._get_cell_value(column)

        return CompensationSchema(value=value, is_taxable=idx in self._fixed_tax_columns)

    def _get_cell_value(self, column: str) -> Decimal:
        value = self._row[self._get_idx(column, calculated=False)]

        if value is None:
            value = Decimal(0)

        return Decimal(value)
