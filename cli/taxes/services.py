from decimal import Decimal

from syriantaxes import (
    Bracket,
    Rounder,
    SocialSecurity,
    calculate_brackets_tax,
    calculate_fixed_tax,
)

from .schemas import Salary


def calculate_gross_taxes(  # noqa: PLR0913
    gross_salary: float,
    gross_compensations: float,
    brackets: list[Bracket],
    fixed_tax_rate: float,
    min_allowed_salary: float,
    tax_rounder: Rounder,
    ss_obj: SocialSecurity,
    ss_salary: float | None = None,
) -> Salary:
    if ss_salary is None:
        brackets_tax = calculate_brackets_tax(
            gross_salary, brackets, min_allowed_salary, tax_rounder
        )
        ss_deduction = Decimal(0)
    else:
        brackets_tax = calculate_brackets_tax(
            gross_salary,
            brackets,
            min_allowed_salary,
            tax_rounder,
            ss_obj,
            ss_salary,
        )
        ss_deduction = ss_obj.calculate_deduction(ss_salary)

    fixed_tax = calculate_fixed_tax(
        gross_compensations, fixed_tax_rate, tax_rounder
    )

    return Salary(
        gross=Decimal(gross_salary),
        compensations=Decimal(gross_compensations),
        ss_deduction=ss_deduction,
        brackets_tax=brackets_tax,
        fixed_tax=fixed_tax,
    )
