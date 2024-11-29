import math
from dataclasses import InitVar, dataclass, field, asdict

from src.db import Database


db = Database()


@dataclass
class Salary:
    amount: InitVar[int] = 0
    as_net: InitVar[bool] = False
    compensations_rate: InitVar[float] = 0.0
    social_security: InitVar[bool] = False
    social_security_salary: int = 0

    gross_salary: int = field(init=False)
    compensations: int = field(init=False, default=0)
    compensations_to_total: float = field(init=False, default=0)
    total_salary: int = field(init=False)
    social_security_deduction: int = field(init=False, default=0)
    tax: int = field(init=False)
    fixed_tax: int = field(init=False, default=0)
    total_deductions: int = field(init=False)
    net_salary: int = field(init=False)

    def __post_init__(
        self, amount: int, as_net: bool, compensations_rate: float, social_security: int
    ) -> None:
        self.ss_minium_salary = int(db.get_setting("social_security_minimum_salary"))

        if amount < self.ss_minium_salary:
            raise ValueError(
                f"amount must be must be greater or equal to {self.ss_minium_salary}"
            )

        if compensations_rate < 0 or compensations_rate > 1:
            raise ValueError("compensation rate must be between 0 and 1")

        if social_security:
            if self.social_security_salary < self.ss_minium_salary:
                raise ValueError(
                    f"social security salary must be greater or equal to {self.ss_minium_salary}"
                )

        self.ss_deduction_rate: float = float(
            db.get_setting("social_security_deduction_rate")
        )
        self.compensations_rate: float = compensations_rate

        if as_net:
            self._calculate_as_net(amount)
        else:
            self._calculate_as_gross(amount)

        self.total_salary = self.gross_salary + self.compensations
        self.total_deductions = (
            self.social_security_deduction + self.fixed_tax + self.tax
        )
        self.net_salary = (
            self.gross_salary
            + self.compensations
            - self.tax
            - self.fixed_tax
            - self.social_security_deduction
        )
        self.compensations_to_total: float = self.compensations / self.total_salary

    def as_dict(self) -> dict:
        return asdict(self)

    def to_rich_table(self) -> tuple[str]:
        return (
            f"{self.gross_salary:,}",
            f"{self.compensations:,}",
            f"{self.total_salary:,}",
            f"{self.social_security_deduction:,}",
            f"{self.tax:,}",
            f"{self.fixed_tax:,}",
            f"{self.total_deductions:,}",
            f"{self.net_salary:,}",
            f"{self.compensations_to_total:.2%}",
        )

    @property
    def layers(self):
        return db.get_layers()

    def _calculate_as_net(self, amount: int) -> None:
        deduction_rate = float(db.get_setting("compensation_tax_rate"))

        gross_salary = self.round(amount * (1 - self.compensations_rate))
        if gross_salary < self.ss_minium_salary:
            gross_salary = self.ss_minium_salary
        compensations = amount - gross_salary

        self.gross_salary = self._get_gross_fixed_salary(gross_salary)
        self.compensations = self._get_gross_compensation(compensations, deduction_rate)

        ss_deduction: int = self.round(
            self.social_security_salary * self.ss_deduction_rate, 0
        )
        self.social_security_deduction = ss_deduction

        self.tax = self._get_layers_tax(self.gross_salary - ss_deduction)
        self.fixed_tax = self.round(self.compensations * deduction_rate)

    def _calculate_as_gross(self, amount: int) -> None:
        self.gross_salary = amount
        ss_deduction: int = self.round(
            self.social_security_salary * self.ss_deduction_rate, 0
        )
        self.social_security_deduction = ss_deduction
        self.tax = self._get_layers_tax(amount - ss_deduction)

    @staticmethod
    def round(amount: int | float, to: int = 2) -> int | float:
        if to < 0:
            raise ValueError("to arg must be greater or equal than zero")
        factor: int = 1 if to == 0 else int("1" + "0" * to)
        return math.ceil(amount / factor) * factor

    def _get_gross_compensation(self, amount: int, deduction_rate: float) -> int:
        return self.round(amount / (1 - deduction_rate))

    def _get_layers_tax(self, amount: int) -> int:
        tax: int = 0

        for layer in self.layers:
            if layer.from_ <= amount <= layer.to_:
                layer_tax = layer.rate * (amount - layer.from_)
                tax += layer_tax
                return self.round(tax)
            else:
                tax += layer.tax

        return self.round(tax)

    def _get_gross_fixed_salary(self, amount: int) -> int:
        if self._get_layers_tax(amount) == 0:
            return int(round(amount, 0))

        min_amount = amount
        max_amount = round(amount * 1.5, 0)

        while True:
            mid_amount = round((min_amount + max_amount) / 2, 0)
            mid_net = mid_amount - self._get_layers_tax(mid_amount)

            if mid_net > amount:
                max_amount = mid_amount
            elif mid_net < amount:
                min_amount = mid_amount
            else:
                return round(mid_amount)


def generate_sequence_range(
    min_amount: int,
    max_amount: int,
    step: int,
    as_net: bool,
    compensations_rate: float,
) -> list[Salary]:
    ss_minium_salary = int(db.get_setting("social_security_minimum_salary"))

    if min_amount < ss_minium_salary:
        raise ValueError(f"min amount must be greater or equal to {ss_minium_salary}")

    if min_amount > max_amount:
        raise ValueError("min amount must be less than max amount")

    if step <= 0:
        raise ValueError("step must be positive")

    salaries: list[Salary] = []
    for salary in range(min_amount, max_amount + step, step):
        salary = Salary(
            amount=salary,
            as_net=as_net,
            compensations_rate=compensations_rate,
        )
        salaries.append(salary)

    return salaries


def generate_salary_variants(amount: int, accuracy: int = 400) -> list[Salary]:
    ss_minium_salary = int(db.get_setting("social_security_minimum_salary"))
    if amount < ss_minium_salary:
        raise ValueError(f"amount must be greater or equal to {ss_minium_salary}")

    salaries: list[Salary] = []
    for rate in range(0, accuracy + 1):
        compensations_rate = rate / accuracy
        salary = Salary(
            amount=amount,
            as_net=True,
            compensations_rate=compensations_rate,
        )
        salaries.append(salary)

    return salaries
