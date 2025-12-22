# ruff: noqa: B008

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typer_di import Depends, TyperDI

from cli.utils import extract_extension

from .exporters import get_export_fn
from .options import AmountRangeOption, GrossOptions, NetOptions, Options
from .services import calculate_gross_taxes, calculate_net_salaries, calculate_net_salary
from .tables import get_salary_table

app = TyperDI()


@app.callback()
def main() -> None:
    """Calculate taxes for a given gross salary and compensations."""


@app.command(name="gross")
def calculate_gross_taxes_cmd(
    options: Options = Depends(Options), gross_options: GrossOptions = Depends(GrossOptions)
) -> None:
    """Calculate taxes for a given gross salary and compensations."""
    _salary = calculate_gross_taxes(
        gross_salary=gross_options.salary,
        gross_compensations=gross_options.compensations,
        brackets=options.brackets,
        fixed_tax_rate=options.fixed_tax_rate,
        min_allowed_salary=options.min_allowed_salary,
        tax_rounder=options.taxes_rounder,
        ss_obj=gross_options.ss_obj,
        ss_salary=gross_options.ss_salary,
    )

    console = Console()
    table = get_salary_table(_salary, title="Gross Results")

    console.print(table)


@app.command(name="net")
def calculate_net_salary_cmd(
    options: Options = Depends(Options), net_options: NetOptions = Depends(NetOptions)
) -> None:
    """Calculate gross salary and compensations for a given target salary."""
    salary = calculate_net_salary(
        target_salary=net_options.target_salary,
        compensations_rate=net_options.compensations_rate,
        brackets=options.brackets,
        fixed_tax_rate=options.fixed_tax_rate,
        min_allowed_salary=options.min_allowed_salary,
        rounder=options.taxes_rounder,
    )

    console = Console()
    table = get_salary_table(salary, title="Net Results")

    console.print(table)


@app.command(name="ar")
def calculate_net_salaries_cmd(
    ar: AmountRangeOption = Depends(AmountRangeOption), options: Options = Depends(Options)
) -> None:
    """Create salaries from a given amount range."""
    if ar.stop is None:
        message = "You must provide a stop value."
        raise typer.BadParameter(message)

    if ar.step is None:
        message = "You must provide a step value."
        raise typer.BadParameter(message)

    salaries = calculate_net_salaries(
        start=ar.start,
        stop=ar.stop,
        step=ar.step,
        compensations_rate=ar.compensations_rate,
        brackets=options.brackets,
        min_allowed_salary=options.min_allowed_salary,
        fixed_tax_rate=options.fixed_tax_rate,
        rounder=options.taxes_rounder,
    )

    console = Console()

    if ar.export_path is not None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Exporting ... ", total=None)
            export_fn = get_export_fn(extract_extension(ar.export_path))
            export_fn(salaries, ar.export_path)
            console.print(f"✅ Results has been exported to {ar.export_path}")
    else:
        table = get_salary_table(*salaries, title="Net Results")
        console.print(table)
