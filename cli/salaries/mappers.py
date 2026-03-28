from .enums import CalculatedColumn, RawColumn, SettingCell

RAW_COLUMNS_MAPPER = {
    RawColumn.FULLNAME: "E",
    ######
    RawColumn.SS_JOIN_DATE: "L",
    RawColumn.SS_ID: "T",
    RawColumn.SS_SALARY: "U",
    ######
    RawColumn.TU_SALARY: "W",
    ######
    RawColumn.DAYS_OF_WORK_COUNT: "X",
    RawColumn.OVERTIME_DAYS_COUNT: "Y",
    RawColumn.HEALTHY_LEAVES_COUNT: "Z",
    RawColumn.WITHOUT_PAY_LEAVES_COUNT: "AA",
    RawColumn.ADDITIONAL_LEAVES_COUNT: "AB",
    RawColumn.HOURS_COUNT: "AC",
    RawColumn.HOUR_PRICE: "AD",
    ######
    RawColumn.FIXED_SALARY: "AE",
    ######
    RawColumn.COMPENSATION_01: "AF",
    RawColumn.COMPENSATION_02: "AG",
    RawColumn.COMPENSATION_03: "AH",
    RawColumn.COMPENSATION_04: "AI",
    RawColumn.COMPENSATION_05: "AJ",
    RawColumn.COMPENSATION_06: "AK",
    RawColumn.COMPENSATION_07: "AL",
    RawColumn.COMPENSATION_08: "AM",
    RawColumn.COMPENSATION_09: "AN",
    RawColumn.COMPENSATION_10: "AO",
    RawColumn.COMPENSATION_11: "AP",
    RawColumn.COMPENSATION_12: "AQ",
    RawColumn.COMPENSATION_13: "AR",
    RawColumn.COMPENSATION_14: "AS",
    RawColumn.COMPENSATION_15: "AT",
    ######
    RawColumn.ADDITIONAL_COMPENSATION_02: "BR",
    RawColumn.ADDITIONAL_COMPENSATION_01: "BQ",
    RawColumn.ADDITIONAL_COMPENSATION_03: "BS",
    RawColumn.ADDITIONAL_COMPENSATION_04: "BT",
    RawColumn.ADDITIONAL_COMPENSATION_05: "BU",
    RawColumn.ADDITIONAL_COMPENSATION_06: "BV",
    RawColumn.ADDITIONAL_COMPENSATION_07: "BW",
    RawColumn.ADDITIONAL_COMPENSATION_08: "BX",
    RawColumn.ADDITIONAL_COMPENSATION_09: "BY",
    RawColumn.ADDITIONAL_COMPENSATION_10: "BZ",
    ######
    RawColumn.DEDUCTION_01: "CF",
    RawColumn.DEDUCTION_02: "CG",
    RawColumn.DEDUCTION_03: "CL",
    RawColumn.DEDUCTION_04: "CM",
    RawColumn.DEDUCTION_05: "CN",
    RawColumn.DEDUCTION_06: "CO",
    RawColumn.DEDUCTION_07: "CP",
    RawColumn.DEDUCTION_08: "CQ",
    RawColumn.DEDUCTION_09: "CR",
    RawColumn.DEDUCTION_10: "CS",
    RawColumn.DEDUCTION_11: "CT",
    RawColumn.DEDUCTION_12: "CU",
}

CALCULATED_COLUMNS_MAPPER = {
    CalculatedColumn.HOURS: "AW",
    CalculatedColumn.FIXED_SALARY: "AX",
    ######
    CalculatedColumn.COMPENSATION_01: "AY",
    CalculatedColumn.COMPENSATION_02: "AZ",
    CalculatedColumn.COMPENSATION_03: "BA",
    CalculatedColumn.COMPENSATION_04: "BB",
    CalculatedColumn.COMPENSATION_05: "BC",
    CalculatedColumn.COMPENSATION_06: "BD",
    CalculatedColumn.COMPENSATION_07: "BE",
    CalculatedColumn.COMPENSATION_08: "BF",
    CalculatedColumn.COMPENSATION_09: "BG",
    CalculatedColumn.COMPENSATION_10: "BH",
    CalculatedColumn.COMPENSATION_11: "BI",
    CalculatedColumn.COMPENSATION_12: "BJ",
    CalculatedColumn.COMPENSATION_13: "BK",
    CalculatedColumn.COMPENSATION_14: "BL",
    CalculatedColumn.COMPENSATION_15: "BM",
    ######
    CalculatedColumn.OVERTIME: "BO",
    CalculatedColumn.LEAVES: "BP",
    ######
    CalculatedColumn.TOTAL: "CA",
    ######
    CalculatedColumn.SS_DEDUCTION: "CB",
    ######
    CalculatedColumn.TU_MONTHLY_DEDUCTION: "CD",
    CalculatedColumn.TU_PENSION_DEDUCTION: "CE",
    ######
    CalculatedColumn.BRACKETS_TAX: "CH",
    CalculatedColumn.FIXED_TAX: "CI",
    ######
    CalculatedColumn.HEALTHY_LEAVES: "CJ",
    CalculatedColumn.WITHOUT_PAY_LEAVES: "CK",
    ######
    CalculatedColumn.DEDUCTIONS: "CL",
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
