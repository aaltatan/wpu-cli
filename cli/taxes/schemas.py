from pydantic import BaseModel, Field


class Gross(BaseModel):
    salary: float
    compensations: float
    total: float
    salary_rate_of_total: float = Field(alias="salaryRateOfTotal")
    compensations_rate_of_total: float = Field(alias="compensationsRateOfTotal")


class Taxes(BaseModel):
    brackets: float
    fixed: float
    total: float


class SocialSecurity(BaseModel):
    salary: float
    deduction: float
    minimum_taxable_salary: float = Field(alias="minimumTaxableSalary")


class Deductions(BaseModel):
    taxes: Taxes
    social_security: SocialSecurity = Field(alias="socialSecurity")
    total: float


class Salary(BaseModel):
    gross: Gross
    deductions: Deductions
    net: float

    @classmethod
    def from_response(cls, response: dict) -> "Salary":
        return cls(**response["data"])

    @classmethod
    def from_bulk_response(cls, response: dict) -> list["Salary"]:
        return [cls(**salary) for salary in response["data"]]

    def to_list(self) -> list[float]:
        return [
            self.gross.salary,
            self.gross.compensations,
            self.gross.total,
            self.deductions.social_security.deduction,
            self.deductions.taxes.brackets,
            self.deductions.taxes.fixed,
            self.deductions.total,
            self.net,
            self.gross.compensations_rate_of_total,
        ]

    def to_rich_table_row(self) -> tuple[str, ...]:
        return (
            f"{self.gross.salary:,}",
            f"{self.gross.compensations:,}",
            f"{self.gross.total:,}",
            f"{self.deductions.social_security.deduction:,}",
            f"{self.deductions.taxes.brackets:,}",
            f"{self.deductions.taxes.fixed:,}",
            f"{self.deductions.total:,}",
            f"{self.net:,}",
            f"{self.gross.compensations_rate_of_total:.2%}",
        )
