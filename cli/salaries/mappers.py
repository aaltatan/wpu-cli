from .enums import RawColumn, SettingCell

# column index - 5 in Salaries.xlsb

RAW_COLUMNS_MAPPER = {
    RawColumn.FULLNAME: 0,
    ######
    RawColumn.SS_ID: 15,
    RawColumn.SS_SALARY: 16,
    ######
    RawColumn.TU_SALARY: 18,
    ######
    RawColumn.DAYS_OF_WORK_COUNT: 19,
    RawColumn.OVERTIME_DAYS_COUNT: 20,
    RawColumn.HEALTHY_LEAVES_COUNT: 21,
    RawColumn.WITHOUT_PAY_LEAVES_COUNT: 22,
    RawColumn.ADDITIONAL_LEAVES_COUNT: 23,
    RawColumn.HOURS_COUNT: 24,
    RawColumn.HOUR_PRICE: 25,
    ######
    RawColumn.FIXED_SALARY: 26,
    ######
    RawColumn.COMPENSATION_01: 27,
    RawColumn.COMPENSATION_02: 28,
    RawColumn.COMPENSATION_03: 29,
    RawColumn.COMPENSATION_04: 30,
    RawColumn.COMPENSATION_05: 31,
    RawColumn.COMPENSATION_06: 32,
    RawColumn.COMPENSATION_07: 33,
    RawColumn.COMPENSATION_08: 34,
    RawColumn.COMPENSATION_09: 35,
    RawColumn.COMPENSATION_10: 36,
    RawColumn.COMPENSATION_11: 37,
    RawColumn.COMPENSATION_12: 38,
    RawColumn.COMPENSATION_13: 39,
    RawColumn.COMPENSATION_14: 40,
    RawColumn.COMPENSATION_15: 41,
    ######
    RawColumn.ADDITIONAL_COMPENSATION_01: 64,
    RawColumn.ADDITIONAL_COMPENSATION_02: 65,
    RawColumn.ADDITIONAL_COMPENSATION_03: 66,
    RawColumn.ADDITIONAL_COMPENSATION_04: 67,
    RawColumn.ADDITIONAL_COMPENSATION_05: 68,
    RawColumn.ADDITIONAL_COMPENSATION_06: 69,
    RawColumn.ADDITIONAL_COMPENSATION_07: 70,
    RawColumn.ADDITIONAL_COMPENSATION_08: 71,
    RawColumn.ADDITIONAL_COMPENSATION_09: 72,
    RawColumn.ADDITIONAL_COMPENSATION_10: 73,
    ######
    RawColumn.DEDUCTION_01: 79,
    RawColumn.DEDUCTION_02: 80,
    RawColumn.DEDUCTION_03: 85,
    RawColumn.DEDUCTION_04: 86,
    RawColumn.DEDUCTION_05: 87,
    RawColumn.DEDUCTION_06: 88,
    RawColumn.DEDUCTION_07: 89,
    RawColumn.DEDUCTION_08: 90,
    RawColumn.DEDUCTION_09: 91,
    RawColumn.DEDUCTION_10: 92,
    RawColumn.DEDUCTION_11: 93,
    RawColumn.DEDUCTION_12: 94,
}


SETTINGS_CELLS_MAPPER = {
    SettingCell.FIXED_TAX_RATE: "F7",
    SettingCell.SS_DEDUCTION_RATE: "F9",
    SettingCell.TU_MONTHLY_DEDUCTION_RATE: "F13",
    SettingCell.TU_PENSION_DEDUCTION_RATE: "F15",
    SettingCell.HEALTHY_LEAVES_RATE: "F17",
    SettingCell.HEALTHY_LEAVES_BASED_ON: "G17",
    SettingCell.DAYS_OF_MONTH: "F19",
    SettingCell.LEAVES_WITHOUT_PAY_RATE: "F21",
    SettingCell.LEAVES_WITHOUT_PAY_BASED_ON: "G21",
    SettingCell.OVERTIME_RATE: "F23",
    SettingCell.OVERTIME_BASED_ON: "G23",
    SettingCell.ADDITIONAL_LEAVES_RATE: "F25",
    SettingCell.ADDITIONAL_LEAVES_BASED_ON: "G25",
    SettingCell.MIN_SS_SALARY: "F29",
}


FIXED_TAX_COLUMNS_RANGE = "I13:I25"

BRACKETS_RANGE = "I28:K38"

CALCULATED_START_COLUMN = "AW"
CALCULATED_END_COLUMN = "CW"
