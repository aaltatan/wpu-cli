# ruff: noqa: B008

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from syriantaxes import SocialSecurity
from typer_di import Depends, TyperDI

from cli.utils import extract_extension

from .exporters import get_export_fn
from .options import (
    AmountRange,
    CompensationsRateOption,
    ExportPathOption,
    GrossCompensationsArgument,
    GrossSalaryArgument,
    Options,
    SocialSecuritySalaryOption,
    TargetSalaryArgument,
    get_amount_range,
    get_options,
    get_ss_obj,
)
from .services import (
    calculate_gross_taxes,
    calculate_net_salaries_from_amount_range,
    calculate_net_salary,
)
from .tables import get_salary_table

app = TyperDI()


@app.callback()
def main() -> None:
    """Calculate taxes for a given gross salary and compensations."""


@app.command(name="gross")
def calculate_gross_taxes_command(
    salary: GrossSalaryArgument,
    compensations: GrossCompensationsArgument = 0,
    options: Options = Depends(get_options),
    ss_obj: SocialSecurity = Depends(get_ss_obj),
    ss_salary: SocialSecuritySalaryOption = None,
):
    """Calculate taxes for a given gross salary and compensations."""
    _salary = calculate_gross_taxes(
        gross_salary=salary,
        gross_compensations=compensations,
        brackets=options.brackets,
        fixed_tax_rate=options.fixed_tax_rate,
        min_allowed_salary=options.min_allowed_salary,
        tax_rounder=options.taxes_rounder,
        ss_obj=ss_obj,
        ss_salary=ss_salary,
    )

    console = Console()
    table = get_salary_table(_salary, title="Gross Results")

    console.print(table)


@app.command(name="net")
def calculate_net_salary_command(
    target_salary: TargetSalaryArgument,
    compensations_rate: CompensationsRateOption,
    options: Options = Depends(get_options),
):
    """Calculate gross salary and compensations for a given target salary."""
    salary = calculate_net_salary(
        target_salary=target_salary,
        compensations_rate=compensations_rate,
        brackets=options.brackets,
        fixed_tax_rate=options.fixed_tax_rate,
        min_allowed_salary=options.min_allowed_salary,
        rounder=options.taxes_rounder,
    )

    console = Console()
    table = get_salary_table(salary, title="Net Results")

    console.print(table)


@app.command(name="ar")
def calculate_net_salaries_from_amount_range_command(
    compensations_rate: CompensationsRateOption,
    ar: AmountRange = Depends(get_amount_range),
    options: Options = Depends(get_options),
    export_path: ExportPathOption = None,
):
    """Create salaries from a given amount range."""
    if ar.stop is None:
        message = "You must provide a stop value."
        raise typer.BadParameter(message)

    if ar.step is None:
        message = "You must provide a step value."
        raise typer.BadParameter(message)

    salaries = calculate_net_salaries_from_amount_range(
        start=ar.start,
        stop=ar.stop,
        step=ar.step,
        compensations_rate=compensations_rate,
        brackets=options.brackets,
        min_allowed_salary=options.min_allowed_salary,
        fixed_tax_rate=options.fixed_tax_rate,
        rounder=options.taxes_rounder,
    )

    console = Console()

    if export_path is not None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Exporting ... ", total=None)
            export_fn = get_export_fn(extract_extension(export_path))
            export_fn(salaries, export_path)
            console.print(f"✅ Results has been exported to {export_path}")
    else:
        table = get_salary_table(*salaries, title="Net Results")
        console.print(table)
