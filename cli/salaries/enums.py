from enum import StrEnum, auto


class RawColumn(StrEnum):
    SS_JOIN_DATE = auto()
    SS_ID = auto()
    SS_SALARY = auto()

    TU_SALARY = auto()

    DAYS_OF_WORK_COUNT = auto()
    OVERTIME_DAYS_COUNT = auto()
    HEALTHY_LEAVES_COUNT = auto()
    WITHOUT_PAY_LEAVES_COUNT = auto()
    ADDITIONAL_LEAVES_COUNT = auto()

    HOURS_COUNT = auto()
    HOUR_PRICE = auto()

    FIXED_SALARY = auto()
    COMPENSATION_01 = auto()
    COMPENSATION_02 = auto()
    COMPENSATION_03 = auto()
    COMPENSATION_04 = auto()
    COMPENSATION_05 = auto()
    COMPENSATION_06 = auto()
    COMPENSATION_07 = auto()
    COMPENSATION_08 = auto()
    COMPENSATION_09 = auto()
    COMPENSATION_10 = auto()
    COMPENSATION_11 = auto()
    COMPENSATION_12 = auto()
    COMPENSATION_13 = auto()
    COMPENSATION_14 = auto()
    COMPENSATION_15 = auto()

    ADDITIONAL_COMPENSATION_01 = auto()
    ADDITIONAL_COMPENSATION_02 = auto()
    ADDITIONAL_COMPENSATION_03 = auto()
    ADDITIONAL_COMPENSATION_04 = auto()
    ADDITIONAL_COMPENSATION_05 = auto()
    ADDITIONAL_COMPENSATION_06 = auto()
    ADDITIONAL_COMPENSATION_07 = auto()
    ADDITIONAL_COMPENSATION_08 = auto()
    ADDITIONAL_COMPENSATION_09 = auto()
    ADDITIONAL_COMPENSATION_10 = auto()

    DEDUCTION_01 = auto()
    DEDUCTION_02 = auto()

    DEDUCTION_03 = auto()
    DEDUCTION_04 = auto()
    DEDUCTION_05 = auto()
    DEDUCTION_06 = auto()
    DEDUCTION_07 = auto()
    DEDUCTION_08 = auto()
    DEDUCTION_09 = auto()
    DEDUCTION_10 = auto()
    DEDUCTION_11 = auto()
    DEDUCTION_12 = auto()


class SettingCell(StrEnum):
    FIXED_TAX_RATE = auto()

    SS_DEDUCTION_RATE = auto()

    TU_MONTHLY_DEDUCTION_RATE = auto()
    TU_PENSION_DEDUCTION_RATE = auto()

    HEALTHY_LEAVES_RATE = auto()
    HEALTHY_LEAVES_BASED_ON = auto()

    DAYS_OF_MONTH = auto()

    LEAVES_WITHOUT_PAY_RATE = auto()
    LEAVES_WITHOUT_PAY_BASED_ON = auto()

    OVERTIME_RATE = auto()
    OVERTIME_BASED_ON = auto()

    ADDITIONAL_LEAVES_RATE = auto()
    ADDITIONAL_LEAVES_BASED_ON = auto()

    MIN_SS_SALARY = auto()
