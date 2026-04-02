from .types import Column, SettingsSheetAddress

# column index - 5 in Salaries.xlsb

COLUMNS_MAPPER: Column = {
    "fullname": 0,
    "status": 3,
    ######
    "ss_id": 15,
    "ss_salary": 16,
    ######
    "tu_salary": 18,
    ######
    "days_of_work_count": 19,
    "overtime_days_count": (20, 62),
    "healthy_leaves_count": (21, 83),
    "without_pay_leaves_count": (22, 84),
    "additional_leaves_count": (23, 63),
    "hours_count": (24, 44),
    "hour_price": 25,
    ######
    "fixed_salary": 26,
    ######
    "compensation_01": (27, 46),
    "compensation_02": (28, 47),
    "compensation_03": (29, 48),
    "compensation_04": (30, 49),
    "compensation_05": (31, 50),
    "compensation_06": (32, 51),
    "compensation_07": (33, 52),
    "compensation_08": (34, 53),
    "compensation_09": (35, 54),
    "compensation_10": (36, 55),
    "compensation_11": (37, 56),
    "compensation_12": (38, 57),
    "compensation_13": (39, 58),
    "compensation_14": (40, 59),
    "compensation_15": (41, 60),
    ######
    "additional_compensation_01": 64,
    "additional_compensation_02": 65,
    "additional_compensation_03": 66,
    "additional_compensation_04": 67,
    "additional_compensation_05": 68,
    "additional_compensation_06": 69,
    "additional_compensation_07": 70,
    "additional_compensation_08": 71,
    "additional_compensation_09": 72,
    "additional_compensation_10": 73,
    ######
    "deduction_01": 79,
    "deduction_02": 80,
    "deduction_03": 85,
    "deduction_04": 86,
    "deduction_05": 87,
    "deduction_06": 88,
    "deduction_07": 89,
    "deduction_08": 90,
    "deduction_09": 91,
    "deduction_10": 92,
    "deduction_11": 93,
    "deduction_12": 94,
}


SETTINGS_MAPPER: SettingsSheetAddress = {
    "fixed_tax_rate": "F7",
    "ss_deduction_rate": "F9",
    "tu_monthly_deduction_rate": "F13",
    "tu_pension_deduction_rate": "F15",
    "healthy_leaves_rate": "F17",
    "healthy_leaves_based_on": "G17",
    "days_of_month": "F19",
    "leaves_without_pay_rate": "F21",
    "leaves_without_pay_based_on": "G21",
    "overtime_rate": "F23",
    "overtime_based_on": "G23",
    "additional_leaves_rate": "F25",
    "additional_leaves_based_on": "G25",
    "min_ss_salary": "F29",
    "min_allowed_salary": "F33",
    "fixed_tax_columns_range": "I13:I25",
    "brackets_range": "I28:K38",
}
