import typer
from rich.console import Console

from .callbacks import app_callback
from .options import (
    GrossCompensationsOption,
    GrossSalaryArgument,
    SocialSecuritySalaryOption,
)
from .services import calculate_gross_taxes
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
