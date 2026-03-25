from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class SocialSecurity(BaseModel):
    join_date: datetime
    ssid: str
    salary: Decimal


class TeachersUnion(BaseModel):
    salary: Decimal


class Compensation(BaseModel):
    value: Decimal = Decimal(0)
    is_taxable: bool = False


class SalaryIn(BaseModel):
    fullname: str

    days_of_work_count: Decimal
    overtime_days_count: Decimal
    healthy_leaves_count: Decimal
    without_pay_leaves_count: Decimal
    additional_leaves_count: Decimal

    hours_count: Decimal
    hour_price: Decimal

    fixed_salary: Decimal
    compensation_01: Compensation
    compensation_02: Compensation
    compensation_03: Compensation
    compensation_04: Compensation
    compensation_05: Compensation
    compensation_06: Compensation
    compensation_07: Compensation
    compensation_08: Compensation
    compensation_09: Compensation
    compensation_10: Compensation
    compensation_11: Compensation
    compensation_12: Compensation
    compensation_13: Compensation
    compensation_14: Compensation
    compensation_15: Compensation

    additional_compensation_01: Compensation | None = None
    additional_compensation_02: Compensation | None = None
    additional_compensation_03: Compensation | None = None
    additional_compensation_04: Compensation | None = None
    additional_compensation_05: Compensation | None = None
    additional_compensation_06: Compensation | None = None
    additional_compensation_07: Compensation | None = None
    additional_compensation_08: Compensation | None = None
    additional_compensation_09: Compensation | None = None
    additional_compensation_10: Compensation | None = None

    deduction_01: Compensation | None = None
    deduction_02: Compensation | None = None

    deduction_03: Compensation | None = None
    deduction_04: Compensation | None = None
    deduction_05: Compensation | None = None
    deduction_06: Compensation | None = None
    deduction_07: Compensation | None = None
    deduction_08: Compensation | None = None
    deduction_09: Compensation | None = None
    deduction_10: Compensation | None = None
    deduction_11: Compensation | None = None
    deduction_12: Compensation | None = None

    social_security: SocialSecurity | None = None
    teachers_union: TeachersUnion | None = None


class SalaryOut(BaseModel):
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

    overtime: Decimal = Decimal(0)
    leaves: Decimal = Decimal(0)

    total: Decimal = Decimal(0)

    ss_deduction: Decimal = Decimal(0)

    tu_monthly_deduction: Decimal = Decimal(0)
    tu_pension_deduction: Decimal = Decimal(0)

    brackets_tax: Decimal = Decimal(0)
    fixed_tax: Decimal = Decimal(0)

    healthy_leaves: Decimal = Decimal(0)
    without_pay_leaves: Decimal = Decimal(0)

    deductions: Decimal = Decimal(0)

    net: Decimal = Decimal(0)
