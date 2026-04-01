from decimal import Decimal

from syriantaxes import Rounder, SocialSecurity, calculate_brackets_tax, calculate_fixed_tax

from .models import BasedOnType, CompensationSchema, SalaryInSchema, SalaryOutSchema, SettingsSchema


class SalaryCalculator:
    def __init__(
        self,
        in_schema: SalaryInSchema,
        settings: SettingsSchema,
        calculation_rounder: Rounder,
        taxes_rounder: Rounder,
        ss_obj: SocialSecurity,
    ) -> None:
        self._row = in_schema
        self._settings = settings
        self._calculation_rounder = calculation_rounder
        self._taxes_rounder = taxes_rounder
        self._ss_obj = ss_obj
        self._fixed_tax = Decimal(0)

    def calculate(self) -> SalaryOutSchema:  # noqa: PLR0915
        hours = self._calc_qty(self._row.hours_count, self._row.hour_price.value)
        fixed_salary = self._calc_days_based_compensation(self._row.fixed_salary)
        compensation_01 = self._calc_days_based_compensation(self._row.compensation_01.value)
        compensation_02 = self._calc_days_based_compensation(self._row.compensation_02.value)
        compensation_03 = self._calc_days_based_compensation(self._row.compensation_03.value)
        compensation_04 = self._calc_days_based_compensation(self._row.compensation_04.value)
        compensation_05 = self._calc_days_based_compensation(self._row.compensation_05.value)
        compensation_06 = self._calc_days_based_compensation(self._row.compensation_06.value)
        compensation_07 = self._calc_days_based_compensation(self._row.compensation_07.value)
        compensation_08 = self._calc_days_based_compensation(self._row.compensation_08.value)
        compensation_09 = self._calc_days_based_compensation(self._row.compensation_09.value)
        compensation_10 = self._calc_days_based_compensation(self._row.compensation_10.value)
        compensation_11 = self._calc_days_based_compensation(self._row.compensation_11.value)
        compensation_12 = self._calc_days_based_compensation(self._row.compensation_12.value)
        compensation_13 = self._calc_days_based_compensation(self._row.compensation_13.value)
        compensation_14 = self._calc_days_based_compensation(self._row.compensation_14.value)
        compensation_15 = self._calc_days_based_compensation(self._row.compensation_15.value)
        overtime = self._calc_salary_components_based_compensation(
            self._row.overtime_days_count.value,
            rate=self._settings.overtime_rate,
            based_on=self._settings.overtime_based_on,
        )
        leaves = self._calc_salary_components_based_compensation(
            self._row.healthy_leaves_count.value,
            rate=self._settings.healthy_leaves_rate,
            based_on=self._settings.healthy_leaves_based_on,
        )
        additional_compensation_01 = self._calc_comp(self._row.additional_compensation_01)
        additional_compensation_02 = self._calc_comp(self._row.additional_compensation_02)
        additional_compensation_03 = self._calc_comp(self._row.additional_compensation_03)
        additional_compensation_04 = self._calc_comp(self._row.additional_compensation_04)
        additional_compensation_05 = self._calc_comp(self._row.additional_compensation_05)
        additional_compensation_06 = self._calc_comp(self._row.additional_compensation_06)
        additional_compensation_07 = self._calc_comp(self._row.additional_compensation_07)
        additional_compensation_08 = self._calc_comp(self._row.additional_compensation_08)
        additional_compensation_09 = self._calc_comp(self._row.additional_compensation_09)
        additional_compensation_10 = self._calc_comp(self._row.additional_compensation_10)

        total = (
            hours
            + fixed_salary
            + compensation_01
            + compensation_02
            + compensation_03
            + compensation_04
            + compensation_05
            + compensation_06
            + compensation_07
            + compensation_08
            + compensation_09
            + compensation_10
            + compensation_11
            + compensation_12
            + compensation_13
            + compensation_14
            + compensation_15
            + overtime
            + leaves
            + (additional_compensation_01 or Decimal(0))
            + (additional_compensation_02 or Decimal(0))
            + (additional_compensation_03 or Decimal(0))
            + (additional_compensation_04 or Decimal(0))
            + (additional_compensation_05 or Decimal(0))
            + (additional_compensation_06 or Decimal(0))
            + (additional_compensation_07 or Decimal(0))
            + (additional_compensation_08 or Decimal(0))
            + (additional_compensation_09 or Decimal(0))
            + (additional_compensation_10 or Decimal(0))
        )

        if self._row.social_security != 0:
            ss_deduction = self._ss_obj.calculate_deduction(self._row.social_security)
        else:
            ss_deduction = Decimal(0)

        tu_monthly_deduction = self._calculation_rounder.round(
            self._row.teachers_union * self._settings.tu_monthly_deduction_rate
        )
        tu_pension_deduction = self._calculation_rounder.round(
            self._row.teachers_union * self._settings.tu_pension_deduction_rate
        )

        deduction_01 = self._calc_comp(self._row.deduction_01)
        deduction_02 = self._calc_comp(self._row.deduction_02)
        deduction_03 = self._calc_comp(self._row.deduction_03)
        deduction_04 = self._calc_comp(self._row.deduction_04)
        deduction_05 = self._calc_comp(self._row.deduction_05)
        deduction_06 = self._calc_comp(self._row.deduction_06)
        deduction_07 = self._calc_comp(self._row.deduction_07)
        deduction_08 = self._calc_comp(self._row.deduction_08)
        deduction_09 = self._calc_comp(self._row.deduction_09)
        deduction_10 = self._calc_comp(self._row.deduction_10)
        deduction_11 = self._calc_comp(self._row.deduction_11)
        deduction_12 = self._calc_comp(self._row.deduction_12)

        healthy_leaves = self._calc_salary_components_based_compensation(
            self._row.healthy_leaves_count.value,
            rate=self._settings.healthy_leaves_rate,
            based_on=self._settings.healthy_leaves_based_on,
        )

        without_pay_leaves = self._calc_salary_components_based_compensation(
            self._row.without_pay_leaves_count.value,
            rate=self._settings.leaves_without_pay_rate,
            based_on=self._settings.leaves_without_pay_based_on,
        )

        brackets_tax_kwargs = {
            "amount": self._row.fixed_salary,
            "brackets": self._settings.brackets,
            "min_allowed_salary": self._settings.min_allowed_salary,
            "rounder": self._taxes_rounder,
        }

        if self._row.social_security:
            brackets_tax_kwargs["ss_obj"] = self._ss_obj
            brackets_tax_kwargs["ss_salary"] = self._row.social_security

        brackets_tax = calculate_brackets_tax(**brackets_tax_kwargs)

        fixed_tax = (
            self._calc_fixed_tax(hours, self._row.hour_price)
            + self._calc_fixed_tax(compensation_01, self._row.compensation_01)
            + self._calc_fixed_tax(compensation_02, self._row.compensation_02)
            + self._calc_fixed_tax(compensation_03, self._row.compensation_03)
            + self._calc_fixed_tax(compensation_04, self._row.compensation_04)
            + self._calc_fixed_tax(compensation_05, self._row.compensation_05)
            + self._calc_fixed_tax(compensation_06, self._row.compensation_06)
            + self._calc_fixed_tax(compensation_07, self._row.compensation_07)
            + self._calc_fixed_tax(compensation_08, self._row.compensation_08)
            + self._calc_fixed_tax(compensation_09, self._row.compensation_09)
            + self._calc_fixed_tax(compensation_10, self._row.compensation_10)
            + self._calc_fixed_tax(compensation_11, self._row.compensation_11)
            + self._calc_fixed_tax(compensation_12, self._row.compensation_12)
            + self._calc_fixed_tax(compensation_13, self._row.compensation_13)
            + self._calc_fixed_tax(compensation_14, self._row.compensation_14)
            + self._calc_fixed_tax(compensation_15, self._row.compensation_15)
            + self._calc_fixed_tax(overtime, self._row.overtime_days_count)
            + self._calc_fixed_tax(leaves, self._row.healthy_leaves_count)
            + self._calc_fixed_tax(additional_compensation_01, self._row.additional_compensation_01)
            + self._calc_fixed_tax(additional_compensation_02, self._row.additional_compensation_02)
            + self._calc_fixed_tax(additional_compensation_03, self._row.additional_compensation_03)
            + self._calc_fixed_tax(additional_compensation_04, self._row.additional_compensation_04)
            + self._calc_fixed_tax(additional_compensation_05, self._row.additional_compensation_05)
            + self._calc_fixed_tax(additional_compensation_06, self._row.additional_compensation_06)
            + self._calc_fixed_tax(additional_compensation_07, self._row.additional_compensation_07)
            + self._calc_fixed_tax(additional_compensation_08, self._row.additional_compensation_08)
            + self._calc_fixed_tax(additional_compensation_09, self._row.additional_compensation_09)
            + self._calc_fixed_tax(additional_compensation_10, self._row.additional_compensation_10)
            + self._calc_fixed_tax(deduction_01, self._row.deduction_01)
            + self._calc_fixed_tax(deduction_02, self._row.deduction_02)
            + self._calc_fixed_tax(healthy_leaves, self._row.healthy_leaves_count)
            + self._calc_fixed_tax(without_pay_leaves, self._row.without_pay_leaves_count)
            + self._calc_fixed_tax(deduction_03, self._row.deduction_03)
            + self._calc_fixed_tax(deduction_04, self._row.deduction_04)
            + self._calc_fixed_tax(deduction_05, self._row.deduction_05)
            + self._calc_fixed_tax(deduction_06, self._row.deduction_06)
            + self._calc_fixed_tax(deduction_07, self._row.deduction_07)
            + self._calc_fixed_tax(deduction_08, self._row.deduction_08)
            + self._calc_fixed_tax(deduction_09, self._row.deduction_09)
            + self._calc_fixed_tax(deduction_10, self._row.deduction_10)
            + self._calc_fixed_tax(deduction_11, self._row.deduction_11)
            + self._calc_fixed_tax(deduction_12, self._row.deduction_12)
        )

        deductions = (
            (deduction_01 or Decimal(0))
            + (deduction_02 or Decimal(0))
            + (deduction_03 or Decimal(0))
            + (deduction_04 or Decimal(0))
            + (deduction_05 or Decimal(0))
            + (deduction_06 or Decimal(0))
            + (deduction_07 or Decimal(0))
            + (deduction_08 or Decimal(0))
            + (deduction_09 or Decimal(0))
            + (deduction_10 or Decimal(0))
            + (deduction_11 or Decimal(0))
            + (deduction_12 or Decimal(0))
            + ss_deduction
            + tu_monthly_deduction
            + tu_pension_deduction
            + brackets_tax
            + fixed_tax
            + healthy_leaves
            + without_pay_leaves
        )

        return SalaryOutSchema(
            hours=hours,
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
            overtime=overtime,
            leaves=leaves,
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
            total=total,
            ss_deduction=ss_deduction,
            tu_monthly_deduction=tu_monthly_deduction,
            tu_pension_deduction=tu_pension_deduction,
            deduction_01=deduction_01,
            deduction_02=deduction_02,
            brackets_tax=brackets_tax,
            fixed_tax=fixed_tax,
            healthy_leaves=healthy_leaves,
            without_pay_leaves=without_pay_leaves,
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
            deductions=deductions,
            net=total - deductions,
        )

    def _calc_qty(self, qty: Decimal, value: Decimal) -> Decimal:
        return self._calculation_rounder.round(qty * value)

    def _calc_fixed_tax(
        self, value: Decimal | None, compensation: CompensationSchema | None
    ) -> Decimal:
        zero_rules = [
            lambda: compensation is None,
            lambda: compensation is not None and not compensation.is_taxable,
            lambda: value == 0,
            lambda: value is None,
        ]

        if any(rule() for rule in zero_rules):
            return Decimal(0)

        return calculate_fixed_tax(
            compensation.value,  # type: ignore  # noqa: PGH003
            self._settings.fixed_tax_rate,
            self._taxes_rounder,
        )

    def _calc_comp(self, compensation: CompensationSchema | None) -> Decimal | None:
        if compensation is None:
            return None

        return self._calculation_rounder.round(compensation.value)

    def _calc_days_based_compensation(self, value: Decimal) -> Decimal:
        if self._row.days_of_work_count == self._settings.days_of_month:
            return value

        return self._calculation_rounder.round(
            (value / self._settings.days_of_month) * self._row.days_of_work_count
        )

    def _calc_salary_components_based_compensation(
        self, qty: Decimal, *, rate: Decimal, based_on: BasedOnType
    ) -> Decimal:
        if based_on == "Total":
            return self._calc_qty(qty, self._row.hr_total * rate)

        return self._calc_qty(qty, self._row.fixed_salary * rate)
