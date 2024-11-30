import typer
from rich.console import Console

from .utils import Wb
from ..models import Setting

from .controllers import (
    Salary,
    generate_salary_variants,
    generate_sequence_range,
)
from .tables import table

console = Console()
app = typer.Typer()


@app.command(name="calc")
def calculate() -> None:
    """
    Calculate individual salary
    """
    amount = typer.prompt("Amount", default=1_000_000, type=int)
    as_net: bool = typer.confirm(
        "calculate as net salary?",
        default=True,
    )
    compensations_rate: float = 0.0
    if as_net:
        compensations_rate: float = typer.prompt(
            "compensations rate",
            default=0.25,
            type=float,
        )
    social_security: bool = typer.confirm(
        "social security?",
        default=False,
    )
    social_security_minimum_salary: int = 0
    if social_security:
        social_security_minimum_salary: int = typer.prompt(
            "social security salary",
            default=Setting.get(key="social_security_minimum_salary").value,
            type=int,
        )

    salary = Salary(
        amount,
        as_net,
        compensations_rate,
        social_security,
        social_security_minimum_salary,
    )

    table.add_row(*salary.to_rich_table())
    console.print(table)


@app.command(name="gen-seq")
def _generate_sequence_range(
    excel: bool = False,
    min_amount: int | None = None,
    max_amount: int | None = None,
    step: int | None = None,
    compensations_rate: float | None = None,
    as_net: bool = False,
):
    """
    generate salary sequence starting from min amount to max amount with step.
    """
    min_amount = min_amount or typer.prompt(
        "Min amount",
        default=Setting.get(key="social_security_minimum_salary").value,
        type=int,
    )
    max_amount = max_amount or typer.prompt(
        "Max amount",
        default=min_amount * 10,
        type=int,
    )
    step = step or typer.prompt(
        "Step",
        default=50_000,
        type=int,
    )
    as_net: bool = as_net or typer.confirm(
        "calculate as net salary?",
        default=True,
    )
    compensations_rate: float = 0.0
    if as_net:
        compensations_rate: float = compensations_rate or typer.prompt(
            "compensations rate",
            default=0.25,
            type=float,
        )

    salaries = generate_sequence_range(
        min_amount=min_amount,
        max_amount=max_amount,
        step=step,
        as_net=as_net,
        compensations_rate=compensations_rate,
    )

    for salary in salaries:
        table.add_row(*salary.to_rich_table())

    if excel:
        Wb().save_table(salaries, f"{min_amount}-to-{max_amount}-salaries.xlsx")
        console.print(
            f"Excel file saved to {min_amount}-to-{max_amount}-salaries.xlsx at your Desktop"
        )
    else:
        console.print(table)


@app.command(name="gen-var")
def _generate_salary_variants(
    excel: bool = False, amount: int | None = None, accuracy: int | None = None
):
    """
    Generate salary variants starting from 0 to 100% compensations rate.
    """
    amount = amount or typer.prompt("Amount", default=1_000_000, type=int)
    accuracy = accuracy or typer.prompt("Accuracy", default=100, type=int)

    salaries = generate_salary_variants(amount, accuracy)

    for salary in salaries:
        table.add_row(*salary.to_rich_table())

    if excel:
        Wb().save_table(salaries, f"{amount}-variants.xlsx")
        console.print(f"Excel file saved to {amount}-variants.xlsx at your Desktop")
    else:
        console.print(table)
