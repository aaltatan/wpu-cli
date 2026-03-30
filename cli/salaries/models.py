from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


class CompensationSchema(BaseModel):
    value: Decimal = Decimal(0)
    is_taxable: bool = False


class SalaryInSchema(BaseModel):
    days_of_work_count: Decimal
    overtime_days_count: Decimal
    healthy_leaves_count: Decimal
    without_pay_leaves_count: Decimal
    additional_leaves_count: Decimal

    hours_count: Decimal
    hour_price: Decimal

    fixed_salary: Decimal
    compensation_01: CompensationSchema
    compensation_02: CompensationSchema
    compensation_03: CompensationSchema
    compensation_04: CompensationSchema
    compensation_05: CompensationSchema
    compensation_06: CompensationSchema
    compensation_07: CompensationSchema
    compensation_08: CompensationSchema
    compensation_09: CompensationSchema
    compensation_10: CompensationSchema
    compensation_11: CompensationSchema
    compensation_12: CompensationSchema
    compensation_13: CompensationSchema
    compensation_14: CompensationSchema
    compensation_15: CompensationSchema

    additional_compensation_01: CompensationSchema | None = None
    additional_compensation_02: CompensationSchema | None = None
    additional_compensation_03: CompensationSchema | None = None
    additional_compensation_04: CompensationSchema | None = None
    additional_compensation_05: CompensationSchema | None = None
    additional_compensation_06: CompensationSchema | None = None
    additional_compensation_07: CompensationSchema | None = None
    additional_compensation_08: CompensationSchema | None = None
    additional_compensation_09: CompensationSchema | None = None
    additional_compensation_10: CompensationSchema | None = None

    deduction_01: CompensationSchema | None = None
    deduction_02: CompensationSchema | None = None

    deduction_03: CompensationSchema | None = None
    deduction_04: CompensationSchema | None = None
    deduction_05: CompensationSchema | None = None
    deduction_06: CompensationSchema | None = None
    deduction_07: CompensationSchema | None = None
    deduction_08: CompensationSchema | None = None
    deduction_09: CompensationSchema | None = None
    deduction_10: CompensationSchema | None = None
    deduction_11: CompensationSchema | None = None
    deduction_12: CompensationSchema | None = None

    social_security: Decimal = Decimal(0)
    teachers_union: Decimal = Decimal(0)


class SalaryOutSchema(BaseModel):
    hours: Decimal = Decimal(0)

    fixed_salary: Decimal = Decimal(0)

    compensation_01: Decimal = Decimal(0)
    compensation_02: Decimal = Decimal(0)
    compensation_03: Decimal = Decimal(0)
    compensation_04: Decimal = Decimal(0)
    compensation_05: Decimal = Decimal(0)
    compensation_06: Decimal = Decimal(0)
    compensation_07: Decimal = Decimal(0)
    compensation_08: Decimal = Decimal(0)
    compensation_09: Decimal = Decimal(0)
    compensation_10: Decimal = Decimal(0)
    compensation_11: Decimal = Decimal(0)
    compensation_12: Decimal = Decimal(0)
    compensation_13: Decimal = Decimal(0)
    compensation_14: Decimal = Decimal(0)
    compensation_15: Decimal = Decimal(0)

    unused: Decimal | None = None

    overtime: Decimal = Decimal(0)
    leaves: Decimal = Decimal(0)

    additional_compensation_01: Decimal | None = None
    additional_compensation_02: Decimal | None = None
    additional_compensation_03: Decimal | None = None
    additional_compensation_04: Decimal | None = None
    additional_compensation_05: Decimal | None = None
    additional_compensation_06: Decimal | None = None
    additional_compensation_07: Decimal | None = None
    additional_compensation_08: Decimal | None = None
    additional_compensation_09: Decimal | None = None
    additional_compensation_10: Decimal | None = None

    total: Decimal = Decimal(0)

    ss_deduction: Decimal = Decimal(0)

    unused_2: Decimal | None = None

    tu_monthly_deduction: Decimal = Decimal(0)
    tu_pension_deduction: Decimal = Decimal(0)

    deduction_01: Decimal | None = None
    deduction_02: Decimal | None = None

    brackets_tax: Decimal = Decimal(0)
    fixed_tax: Decimal = Decimal(0)

    healthy_leaves: Decimal = Decimal(0)
    without_pay_leaves: Decimal = Decimal(0)

    deduction_03: Decimal | None = None
    deduction_04: Decimal | None = None
    deduction_05: Decimal | None = None
    deduction_06: Decimal | None = None
    deduction_07: Decimal | None = None
    deduction_08: Decimal | None = None
    deduction_09: Decimal | None = None
    deduction_10: Decimal | None = None
    deduction_11: Decimal | None = None
    deduction_12: Decimal | None = None

    deductions: Decimal = Decimal(0)

    net: Decimal = Decimal(0)

    def as_row(self) -> list[Decimal | None]:
        return [
            self.hours,
            self.fixed_salary,
            self.compensation_01,
            self.compensation_02,
            self.compensation_03,
            self.compensation_04,
            self.compensation_05,
            self.compensation_06,
            self.compensation_07,
            self.compensation_08,
            self.compensation_09,
            self.compensation_10,
            self.compensation_11,
            self.compensation_12,
            self.compensation_13,
            self.compensation_14,
            self.compensation_15,
            self.unused,
            self.overtime,
            self.leaves,
            self.additional_compensation_01,
            self.additional_compensation_02,
            self.additional_compensation_03,
            self.additional_compensation_04,
            self.additional_compensation_05,
            self.additional_compensation_06,
            self.additional_compensation_07,
            self.additional_compensation_08,
            self.additional_compensation_09,
            self.additional_compensation_10,
            self.total,
            self.ss_deduction,
            self.unused_2,
            self.tu_monthly_deduction,
            self.tu_pension_deduction,
            self.deduction_01,
            self.deduction_02,
            self.brackets_tax,
            self.fixed_tax,
            self.healthy_leaves,
            self.without_pay_leaves,
            self.deduction_03,
            self.deduction_04,
            self.deduction_05,
            self.deduction_06,
            self.deduction_07,
            self.deduction_08,
            self.deduction_09,
            self.deduction_10,
            self.deduction_11,
            self.deduction_12,
            self.deductions,
            self.net,
        ]


class BracketSchema(BaseModel):
    min: Decimal
    max: Decimal
    rate: Decimal


class SettingsSchema(BaseModel):
    fixed_tax_rate: Decimal

    ss_deduction_rate: Decimal

    tu_monthly_deduction_rate: Decimal
    tu_pension_deduction_rate: Decimal

    healthy_leaves_rate: Decimal
    healthy_leaves_based_on: Literal["Total", "Salary"]

    days_of_month: Decimal

    leaves_without_pay_rate: Decimal
    leaves_without_pay_based_on: Literal["Total", "Salary"]

    overtime_rate: Decimal
    overtime_based_on: Literal["Total", "Salary"]

    additional_leaves_rate: Decimal
    additional_leaves_based_on: Literal["Total", "Salary"]

    fixed_tax_columns: list[int]
    brackets: list[BracketSchema]

    min_ss_salary: Decimal
