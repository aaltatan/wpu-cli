from dataclasses import dataclass, field, InitVar

from ..taxes.schemas import Layer


@dataclass
class Salary:
    amount: int
    social_security: InitVar[bool] = False
    social_security_salary: int | None = None
    layers: list[Layer] = field(default_factory=list)
    gross_salary = field(init=False)
    compensation = field(init=False)
    layers_tax = field(init=False)
    fixed_tax = field(init=False)

    def _layers_tax(self):
        ...

    def _gross_fixed_salary(self):
        ...
    
    def _gross_salary(self):
        ...

    def __post_init__(self, socials_security: bool):
        if socials_security:
            if self.social_security_salary is None:
                self.social_security_salary = self.amount
        if self.amount < 0:
            raise ValueError("amount must be positive")

        if self.social_security_salary < 0:
            raise ValueError("social_security_salary must be positive")

        if self.social_security_salary > self.amount:
            raise ValueError(
                "social_security_salary must be less than or equal to amount"
            )
