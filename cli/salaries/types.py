from typing import TypedDict


class Column(TypedDict):
    ss_id: int
    ss_salary: int

    tu_salary: int

    days_of_work_count: int
    overtime_days_count: tuple[int, int]
    healthy_leaves_count: tuple[int, int]
    without_pay_leaves_count: tuple[int, int]
    additional_leaves_count: tuple[int, int]

    hours_count: tuple[int, int]
    hour_price: int

    fixed_salary: int

    compensation_01: tuple[int, int]
    compensation_02: tuple[int, int]
    compensation_03: tuple[int, int]
    compensation_04: tuple[int, int]
    compensation_05: tuple[int, int]
    compensation_06: tuple[int, int]
    compensation_07: tuple[int, int]
    compensation_08: tuple[int, int]
    compensation_09: tuple[int, int]
    compensation_10: tuple[int, int]
    compensation_11: tuple[int, int]
    compensation_12: tuple[int, int]
    compensation_13: tuple[int, int]
    compensation_14: tuple[int, int]
    compensation_15: tuple[int, int]

    additional_compensation_01: int
    additional_compensation_02: int
    additional_compensation_03: int
    additional_compensation_04: int
    additional_compensation_05: int
    additional_compensation_06: int
    additional_compensation_07: int
    additional_compensation_08: int
    additional_compensation_09: int
    additional_compensation_10: int

    deduction_01: int
    deduction_02: int

    deduction_03: int
    deduction_04: int
    deduction_05: int
    deduction_06: int
    deduction_07: int
    deduction_08: int
    deduction_09: int
    deduction_10: int
    deduction_11: int
    deduction_12: int


class SettingsSheetAddress(TypedDict):
    fixed_tax_rate: str

    ss_deduction_rate: str

    tu_monthly_deduction_rate: str
    tu_pension_deduction_rate: str

    healthy_leaves_rate: str
    healthy_leaves_based_on: str

    days_of_month: str

    leaves_without_pay_rate: str
    leaves_without_pay_based_on: str

    overtime_rate: str
    overtime_based_on: str

    additional_leaves_rate: str
    additional_leaves_based_on: str

    min_ss_salary: str

    min_allowed_salary: str

    fixed_tax_columns_range: str
    brackets_range: str
