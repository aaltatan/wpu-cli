from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, computed_field

type BasedOnType = Literal["Salary", "Total"]


class CompensationSchema(BaseModel):
    value: Decimal = Decimal(0)
    is_taxable: bool = False


class RowSchema(BaseModel):
    fullname: str
    status: bool

    transfer_type: str

    days_of_work_count: Decimal
    overtime_days_count: CompensationSchema
    healthy_leaves_count: CompensationSchema
    without_pay_leaves_count: CompensationSchema
    additional_leaves_count: CompensationSchema

    hours_count: Decimal
    hour_price: CompensationSchema

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

    @computed_field
    @property
    def hr_total(self) -> Decimal:
        return (
            +self.fixed_salary
            + self.compensation_01.value
            + self.compensation_02.value
            + self.compensation_03.value
            + self.compensation_04.value
            + self.compensation_05.value
            + self.compensation_06.value
            + self.compensation_07.value
            + self.compensation_08.value
            + self.compensation_09.value
            + self.compensation_10.value
            + self.compensation_11.value
            + self.compensation_12.value
            + self.compensation_13.value
            + self.compensation_14.value
            + self.compensation_15.value
        )


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

    def as_row(self) -> list[float]:
        return [
            float(self.hours),
            float(self.fixed_salary),
            float(self.compensation_01),
            float(self.compensation_02),
            float(self.compensation_03),
            float(self.compensation_04),
            float(self.compensation_05),
            float(self.compensation_06),
            float(self.compensation_07),
            float(self.compensation_08),
            float(self.compensation_09),
            float(self.compensation_10),
            float(self.compensation_11),
            float(self.compensation_12),
            float(self.compensation_13),
            float(self.compensation_14),
            float(self.compensation_15),
            float(self.unused or 0),
            float(self.overtime),
            float(self.leaves),
            float(self.additional_compensation_01 or 0),
            float(self.additional_compensation_02 or 0),
            float(self.additional_compensation_03 or 0),
            float(self.additional_compensation_04 or 0),
            float(self.additional_compensation_05 or 0),
            float(self.additional_compensation_06 or 0),
            float(self.additional_compensation_07 or 0),
            float(self.additional_compensation_08 or 0),
            float(self.additional_compensation_09 or 0),
            float(self.additional_compensation_10 or 0),
            float(self.total),
            float(self.ss_deduction),
            float(self.unused_2 or 0),
            float(self.tu_monthly_deduction),
            float(self.tu_pension_deduction),
            float(self.deduction_01 or 0),
            float(self.deduction_02 or 0),
            float(self.brackets_tax),
            float(self.fixed_tax),
            float(self.healthy_leaves),
            float(self.without_pay_leaves),
            float(self.deduction_03 or 0),
            float(self.deduction_04 or 0),
            float(self.deduction_05 or 0),
            float(self.deduction_06 or 0),
            float(self.deduction_07 or 0),
            float(self.deduction_08 or 0),
            float(self.deduction_09 or 0),
            float(self.deduction_10 or 0),
            float(self.deduction_11 or 0),
            float(self.deduction_12 or 0),
            float(self.deductions),
            float(self.net),
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
    healthy_leaves_based_on: BasedOnType

    days_of_month: Decimal

    leaves_without_pay_rate: Decimal
    leaves_without_pay_based_on: BasedOnType

    overtime_rate: Decimal
    overtime_based_on: BasedOnType

    additional_leaves_rate: Decimal
    additional_leaves_based_on: BasedOnType

    fixed_tax_columns: list[int]
    brackets: list[BracketSchema]

    min_ss_salary: Decimal

    min_allowed_salary: Decimal
