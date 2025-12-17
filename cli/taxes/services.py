# ruff: noqa: PLR0913

from decimal import Decimal

from syriantaxes import (
    Bracket,
    Rounder,
    SocialSecurity,
    calculate_brackets_tax,
    calculate_fixed_tax,
    calculate_gross_components,
)

from .schemas import Salary


def calculate_gross_taxes(
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


def calculate_net_salary(
    target_salary: float,
    compensations_rate: float,
    brackets: list[Bracket],
    min_allowed_salary: float,
    fixed_tax_rate: float,
    rounder: Rounder,
) -> Salary:
    gross_salary, gross_compensations = calculate_gross_components(
        target=target_salary,
        compensations_rate=compensations_rate,
        brackets=brackets,
        min_allowed_salary=min_allowed_salary,
        compensations_tax_rate=fixed_tax_rate,
        rounder=rounder,
    )

    brackets_tax = calculate_brackets_tax(
        gross_salary, brackets, min_allowed_salary, rounder
    )
    fixed_tax = calculate_fixed_tax(
        gross_compensations, fixed_tax_rate, rounder
    )

    return Salary(
        gross=Decimal(gross_salary),
        compensations=Decimal(gross_compensations),
        brackets_tax=brackets_tax,
        fixed_tax=fixed_tax,
    )


def calculate_net_salaries_from_amount_range(
    start: float,
    stop: float,
    step: float,
    compensations_rate: float,
    brackets: list[Bracket],
    min_allowed_salary: float,
    fixed_tax_rate: float,
    rounder: Rounder,
) -> list[Salary]:
    return [
        calculate_net_salary(
            target_salary=target,
            compensations_rate=compensations_rate,
            brackets=brackets,
            min_allowed_salary=min_allowed_salary,
            fixed_tax_rate=fixed_tax_rate,
            rounder=rounder,
        )
        for target in range(int(start), int(stop) + 1, int(step))
    ]
