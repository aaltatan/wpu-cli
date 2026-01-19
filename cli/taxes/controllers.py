# ruff: noqa: B008

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from syriantaxes import Bracket, Rounder, SocialSecurity
from typer_di import Depends, TyperDI

from cli.utils import extract_extension

from .options import (
    AmountRange,
    Config,
    Gross,
    Net,
    WritePathOpt,
    get_brackets,
    get_ss_obj,
    get_taxes_rounder,
)
from .services import calculate_gross_taxes, calculate_net_salaries, calculate_net_salary
from .tables import get_salary_table
from .writers import get_write_fn

app = TyperDI()


@app.callback()
def main() -> None:
    """Calculate taxes for a given gross salary and compensations."""


@app.command(name="gross")
def calculate_gross_taxes_cmd(
    config: Config = Depends(Config),
    brackets: list[Bracket] = Depends(get_brackets),
    taxes_rounder: Rounder = Depends(get_taxes_rounder),
    ss_obj: SocialSecurity = Depends(get_ss_obj),
    gross: Gross = Depends(Gross),
) -> None:
    """Calculate taxes for a given gross salary and compensations."""
    _salary = calculate_gross_taxes(
        gross_salary=gross.salary,
        gross_compensations=gross.compensations,
        brackets=brackets,
        fixed_tax_rate=config.fixed_tax_rate,
        min_allowed_salary=config.min_allowed_salary,
        tax_rounder=taxes_rounder,
        ss_obj=ss_obj,
        ss_salary=gross.ss_salary,
    )

    console = Console()
    table = get_salary_table(_salary, title="Gross Results")

    console.print(table)


@app.command(name="net")
def calculate_net_salary_cmd(
    net: Net = Depends(Net),
    brackets: list[Bracket] = Depends(get_brackets),
    taxes_rounder: Rounder = Depends(get_taxes_rounder),
    config: Config = Depends(Config),
) -> None:
    """Calculate gross salary and compensations for a given target salary."""
    salary = calculate_net_salary(
        target_salary=net.target_salary,
        compensations_rate=net.compensations_rate,
        brackets=brackets,
        fixed_tax_rate=config.fixed_tax_rate,
        min_allowed_salary=config.min_allowed_salary,
        rounder=taxes_rounder,
    )

    console = Console()
    table = get_salary_table(salary, title="Net Results")

    console.print(table)


@app.command(name="ar")
def calculate_net_salaries_cmd(
    ar: AmountRange = Depends(AmountRange),
    brackets: list[Bracket] = Depends(get_brackets),
    taxes_rounder: Rounder = Depends(get_taxes_rounder),
    config: Config = Depends(Config),
    write_path: WritePathOpt = None,
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
        brackets=brackets,
        min_allowed_salary=config.min_allowed_salary,
        fixed_tax_rate=config.fixed_tax_rate,
        rounder=taxes_rounder,
    )

    console = Console()

    if write_path is not None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Writing ... ", total=None)
            write_fn = get_write_fn(extract_extension(write_path))
            write_fn(salaries, write_path)
            console.print(f"✅ Results has been written to {write_path}")
    else:
        table = get_salary_table(*salaries, title="Net Results")
        console.print(table)
