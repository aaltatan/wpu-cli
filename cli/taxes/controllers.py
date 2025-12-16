import typer
from rich.console import Console

from .callbacks import app_callback
from .options import (
    CompensationsRateOption,
    GrossCompensationsOption,
    GrossSalaryArgument,
    SocialSecuritySalaryOption,
    TargetSalaryArgument,
)
from .services import calculate_gross_taxes, calculate_net_salary
from .tables import get_salary_table

app = typer.Typer(callback=app_callback)


@app.command(name="gross")
def calculate_gross_taxes_command(
    ctx: typer.Context,
    gross_salary: GrossSalaryArgument,
    gross_compensations: GrossCompensationsOption = 0,
    ss_salary: SocialSecuritySalaryOption = None,
):
    """Calculate taxes for a given gross salary and compensations."""
    salary = calculate_gross_taxes(
        gross_salary=gross_salary,
        gross_compensations=gross_compensations,
        brackets=ctx.obj["brackets"],
        fixed_tax_rate=ctx.obj["fixed_tax_rate"],
        min_allowed_salary=ctx.obj["min_allowed_salary"],
        tax_rounder=ctx.obj["tax_rounder"],
        ss_obj=ctx.obj["ss"],
        ss_salary=ss_salary,
    )

    console = Console()
    table = get_salary_table(salary, title="Gross Results")

    console.print(table)


@app.command(name="net")
def calculate_net_salary_command(
    ctx: typer.Context,
    target_salary: TargetSalaryArgument,
    compensations_rate: CompensationsRateOption,
):
    """Calculate gross salary and compensations for a given target salary."""
    salary = calculate_net_salary(
        target_salary=target_salary,
        compensations_rate=compensations_rate,
        brackets=ctx.obj["brackets"],
        fixed_tax_rate=ctx.obj["fixed_tax_rate"],
        min_allowed_salary=ctx.obj["min_allowed_salary"],
        rounder=ctx.obj["tax_rounder"],
    )

    console = Console()
    table = get_salary_table(salary, title="Net Results")

    console.print(table)
