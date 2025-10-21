from pathlib import Path

import typer
from httpx import ConnectError
from rich.console import Console
from typing_extensions import Annotated

from .exporters import ExportType, get_exporters
from .services import calculate_salary, generate_salaries_by_rate_range, generate_salary
from .tables import table

SSSalaryTyperParam = Annotated[
    int | None, typer.Option("--socialsecurity", "-s", help="Social security salary")
]
TaxIdTyperParam = Annotated[int | None, typer.Option("--taxid", help="Tax id")]
SsIdTyperParam = Annotated[int | None, typer.Option("--ssid", help="SS id")]

console = Console()
app = typer.Typer()


@app.command(name="calc")
def calculate(
    gross_salary: Annotated[
        float,
        typer.Option(
            "--gross",
            "-g",
            help="Gross salary",
            prompt=True,
            envvar="DEFAULT_GROSS_SALARY",
        ),
    ],
    compensations: Annotated[
        float | None, typer.Option("--compensations", "-c", help="Compensations")
    ] = None,
    ss_salary: SSSalaryTyperParam = None,
    tax_id: TaxIdTyperParam = None,
    ss_id: SsIdTyperParam = None,
):
    """
    Calculate individual salary
    """
    try:
        salary = calculate_salary(
            gross_salary=gross_salary,
            compensations=compensations,
            tax_id=tax_id,
            ss_salary=ss_salary,
            ss_id=ss_id,
        )
        table.add_row(*salary.to_rich_table_row())
        console.print(table)
    except ConnectError:
        console.print("❌ [red]Connection error[/red]. Please try again later.")


@app.command(name="gen")
def generate(
    amount: Annotated[
        float,
        typer.Option(
            "--amount",
            "-a",
            help="Target net salary",
            prompt=True,
            envvar="DEFAULT_GENERATE_AMOUNT",
        ),
    ],
    compensations_rate: Annotated[
        float | None,
        typer.Option(
            "--rate",
            "-r",
            help="Compensations rate",
            envvar="DEFAULT_GENERATE_COMPENSATIONS_RATE",
        ),
    ],
    ss_salary: SSSalaryTyperParam = None,
    tax_id: TaxIdTyperParam = None,
    ss_id: SsIdTyperParam = None,
):
    """
    Generate salary.
    """
    try:
        salary = generate_salary(
            amount=amount,
            compensations_rate=compensations_rate,
            tax_id=tax_id,
            ss_salary=ss_salary,
            ss_id=ss_id,
        )
        table.add_row(*salary.to_rich_table_row())
        console.print(table)
    except ConnectError:
        console.print("❌ [red]Connection error[/red]. Please try again later.")


@app.command(name="rr")
def generate_by_rate_range(
    amount: Annotated[
        float,
        typer.Option(
            "--amount",
            "-a",
            help="Target net salary",
            prompt=True,
            envvar="DEFAULT_GENERATE_AMOUNT",
        ),
    ],
    tax_id: TaxIdTyperParam = None,
    start: Annotated[
        int,
        typer.Option(
            "--start",
            help="Start salary",
        ),
    ] = 0,
    end: Annotated[
        int,
        typer.Option(
            "--end",
            help="End salary",
        ),
    ] = 100,
    step: Annotated[
        int,
        typer.Option(
            "--step",
            help="Step",
        ),
    ] = 1,
    export: Annotated[
        ExportType | None,
        typer.Option(
            "--export",
            "-e",
            help="Export type",
        ),
    ] = None,
):
    """
    Generate salary by rate range.
    """
    try:
        salaries = generate_salaries_by_rate_range(
            amount=amount, tax_id=tax_id, start=start, end=end, step=step
        )

        if export is not None:
            path = get_exporters()[export](
                f"rate-range-{amount}-{start}-{end}-{step}",
                salaries,
                Path().home().resolve() / "Desktop",
            )
            console.print(f"file saved successfully to [green]{path}[/green]")
            return

        for salary in salaries:
            table.add_row(*salary.to_rich_table_row())

        console.print(table)

    except ConnectError:
        console.print("❌ [red]Connection error[/red]. Please try again later.")
