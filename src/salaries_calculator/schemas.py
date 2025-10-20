from dataclasses import asdict, dataclass, field


@dataclass
class TaxBracket:
    from_: int
    to_: int
    rate: float


@dataclass
class Salary:
    gross_salary: int
    compensations: int

    social_security_deduction: int
    brackets_tax: int
    fixed_tax: int

    compensations_to_total: float = field(init=False, default=0)
    total_salary: int = field(init=False)
    total_taxes: int = field(init=False)
    total_deductions: int = field(init=False)
    net: int = field(init=False)

    def __post_init__(self) -> None:
        self.total_salary = self.gross_salary + self.compensations
        self.total_taxes = self.fixed_tax + self.brackets_tax
        self.total_deductions = self.social_security_deduction + self.total_taxes
        self.net = self.total_salary - self.total_deductions
        self.compensations_to_total = self.compensations / self.total_salary

    def as_dict(self) -> dict:
        return asdict(self)

    def to_rich_table(self) -> tuple[str]:
        return (
            f"{self.gross_salary:,}",
            f"{self.compensations:,}",
            f"{self.total_salary:,}",
            f"{self.social_security_deduction:,}",
            f"{self.brackets_tax:,}",
            f"{self.fixed_tax:,}",
            f"{self.total_deductions:,}",
            f"{self.net:,}",
            f"{self.compensations_to_total:.2%}",
        )
