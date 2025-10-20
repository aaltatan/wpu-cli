from .exceptions import AmountLessThanSSMinimumError, AmountLessThanZeroError
from .schemas import Salary, TaxBracket
import math
from typing import Callable, Literal

type RoundMethod = Literal["ceil", "floor", "round"]


class Rounder:
    def __init__(self, method: RoundMethod = "ceil", to_nearest: int = 200) -> None:
        self.method = method
        self.to_nearest = to_nearest

        self.methods: dict[RoundMethod, Callable[[int], int]] = {
            "ceil": math.ceil,
            "floor": math.floor,
            "round": round,
        }

    def round(self, amount: int) -> int:
        return self.methods[self.method](amount / self.to_nearest) * self.to_nearest


class SocialSecurity:
    def __init__(
        self, salary: int, min: int, deduction_rate: float, rounder: Rounder
    ) -> None:
        self.salary = salary
        self.min = min
        self.deduction_rate = deduction_rate
        self.rounder = rounder

    def calculate(self) -> int:
        if self.salary < self.min:
            raise AmountLessThanSSMinimumError()

        return self.rounder.round(self.salary * self.deduction_rate)


class Calculator:
    def __init__(
        self,
        brackets: list[TaxBracket],
        fixed_tax_rate: float,
        compensations_rate: float,
        min_salary_allowed: int,
        rounder: Rounder,
        ss: SocialSecurity | None = None,
    ) -> None:
        self.brackets = brackets
        self.fixed_tax_rate = fixed_tax_rate
        self.compensations_rate = compensations_rate
        self.min_salary_allowed = min_salary_allowed
        self.rounder = rounder
        self.ss = ss

    def calculate_gross_fixed_salary(self, amount: int) -> int:
        if self.calculate_layers_tax(amount) == 0:
            return int(round(amount, 0))

        min_amount = amount
        max_amount = round(amount * 1.5, 0)

        while True:
            mid_amount = round((min_amount + max_amount) / 2, 0)
            mid_net = mid_amount - self.calculate_layers_tax(mid_amount)

            if mid_net > amount:
                max_amount = mid_amount
            elif mid_net < amount:
                min_amount = mid_amount
            else:
                return round(mid_amount)

    def calculate_ss_deduction(self) -> int:
        return self.ss.calculate() if self.ss else 0

    def calculate_fixed_tax(self, amount: int) -> int:
        if amount < 0:
            raise AmountLessThanZeroError()

        return self.rounder.round(amount * self.fixed_tax_rate)

    def calculate_gross_compensation(
        self, amount: int, compensations_rate: float
    ) -> int:
        if amount < 0:
            raise AmountLessThanZeroError()

        if compensations_rate is None:
            compensations_rate = self.compensations_rate

        return self.rounder.round(amount / (1 - self.compensations_rate))

    def calculate_layers_tax(self, amount: int) -> int:
        tax: int = 0

        for bracket in self.brackets:
            if bracket.from_ <= amount <= bracket.to_:
                layer_tax = bracket.rate * (amount - bracket.from_)
                tax += layer_tax
                return self.rounder.round(tax)
            else:
                tax += (bracket.to_ - bracket.from_) * bracket.rate

        return self.rounder.round(tax)

    def calculate_salary_components(
        self, amount: int, compensations_rate: float | None = None
    ) -> tuple[int, int]:
        if compensations_rate is None:
            compensations_rate = self.compensations_rate

        gross_salary_before = self.round(amount * (1 - compensations_rate))

        if gross_salary_before < self.min_salary_allowed:
            gross_salary = self.min_salary_allowed
            ss_minium_salary_tax = self.calculate_layers_tax(self.min_salary_allowed)
            compensations_before = (
                amount - self.min_salary_allowed + ss_minium_salary_tax
            )
        else:
            gross_salary = self.calculate_gross_fixed_salary(gross_salary_before)
            compensations_before = amount - gross_salary_before

        self.compensations = self.calculate_gross_compensation(
            compensations_before, compensations_rate
        )

        return gross_salary, compensations_before

    def calculate(self, gross_salary: int, compensations: int = 0) -> Salary:
        if gross_salary < self.min_salary_allowed:
            raise AmountLessThanSSMinimumError()

        taxable_salary = gross_salary
        ss_deduction = 0

        if self.ss:
            ss_deduction = self.calculate_ss_deduction()
            taxable_salary = gross_salary - ss_deduction

        brackets_tax = self.calculate_layers_tax(taxable_salary)
        fixed_tax = self.calculate_fixed_tax(compensations)

        return Salary(
            gross_salary=gross_salary,
            compensations=compensations,
            ss_deduction=ss_deduction,
            brackets_tax=brackets_tax,
            fixed_tax=fixed_tax,
        )

    def generate(self, amount: int, compensations_rate: float | None = None) -> Salary:
        if compensations_rate is None:
            compensations_rate = self.compensations_rate

        gross_salary, compensations = self.calculate_salary_components(
            amount, compensations_rate
        )

        ss_deduction = 0
        if self.ss:
            ss_deduction = self.calculate_ss_deduction()

        brackets_tax = self.calculate_layers_tax(gross_salary)
        fixed_tax = self.calculate_fixed_tax(compensations)

        return Salary(
            gross_salary=gross_salary,
            compensations=compensations,
            ss_deduction=ss_deduction,
            brackets_tax=brackets_tax,
            fixed_tax=fixed_tax,
        )

    def generate_salaries_by_amount_range(
        self, min_amount: int, max_amount: int, step: int
    ) -> list[Salary]:
        if min_amount < self.min_salary_allowed:
            raise AmountLessThanSSMinimumError()

        if min_amount > max_amount:
            raise ValueError("min amount must be less than max amount")

        if step <= 0:
            raise ValueError("step must be positive")

        salaries: list[Salary] = [
            self.generate(amount)
            for amount in range(min_amount, max_amount + step, step)
        ]

        return salaries

    def generate_salaries_by_rate_range(
        self, amount: int, accuracy: int = 400
    ) -> list[Salary]:
        if amount < self.min_salary_allowed:
            raise AmountLessThanSSMinimumError()

        salaries: list[Salary] = []
        for rate in range(0, accuracy + 1):
            compensations_rate = rate / accuracy
            salary = self.generate(amount, compensations_rate=compensations_rate)
            salaries.append(salary)

        return salaries
