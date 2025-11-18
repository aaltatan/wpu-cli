from pathlib import Path
from typing import Annotated

import typer
from httpx import ConnectError
from rich.console import Console

from .exporters import ExportType, get_exporters
from .services import (
    calculate_gross_salary,
    calculate_net_salary,
    generate_salaries_by_amount_range,
    generate_salaries_by_rate_range,
)
from .tables import get_salaries_table

SSSalaryTyperParam = Annotated[
    int | None,
    typer.Option("--socialsecurity", "-s", help="Social security salary"),
]
TaxIdTyperParam = Annotated[int | None, typer.Option("--taxid", help="Tax id")]
SsIdTyperParam = Annotated[int | None, typer.Option("--ssid", help="SS id")]

console = Console()
app = typer.Typer()


@app.command(name="net", help="Calculate net salary from gross inputs")
def calculate_net(
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
        float | None,
        typer.Option("--compensations", "-c", help="Compensations"),
    ] = None,
    ss_salary: SSSalaryTyperParam = None,
    tax_id: TaxIdTyperParam = None,
    ss_id: SsIdTyperParam = None,
):
    try:
        salary = calculate_net_salary(
            gross_salary=gross_salary,
            compensations=compensations,
            tax_id=tax_id,
            ss_salary=ss_salary,
            ss_id=ss_id,
        )
        table = get_salaries_table()
        table.add_row(*salary.to_rich_table_row())
        console.print(table)
    except ConnectError:
        console.print("❌ [red]Connection error[/red]. Please try again later.")


@app.command(name="gross", help="Calculate gross salary from net inputs")
def calculate_gross(
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
    try:
        salary = calculate_gross_salary(
            amount=amount,
            compensations_rate=compensations_rate,
            tax_id=tax_id,
            ss_salary=ss_salary,
            ss_id=ss_id,
        )
        table = get_salaries_table()
        table.add_row(*salary.to_rich_table_row())
        console.print(table)
    except ConnectError:
        console.print("❌ [red]Connection error[/red]. Please try again later.")


@app.command(name="rr", help="Generate salary by rate range.")
def generate_by_rate_range(  # noqa: PLR0913
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
    stop: Annotated[
        int,
        typer.Option(
            "--stop",
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
    if start > stop:
        message = "❌ Start must be less than stop"
        raise ValueError(message)

    if step > stop:
        message = "❌ Step must be less than stop"
        raise ValueError(message)

    if (stop - start) < step:
        message = "❌ Stop - Start must be greater than step"
        raise ValueError(message)

    try:
        salaries = generate_salaries_by_rate_range(
            amount=amount, tax_id=tax_id, start=start, stop=stop, step=step
        )

        if export is not None:
            filename = f"rate-range-{amount}-{start}-{stop}-{step}"
            save_path = Path().home().resolve() / "Desktop"
            path = get_exporters()[export](filename, salaries, save_path)
            console.print(
                f"💾 file saved successfully to [green]{path}[/green]"
            )
            return

        table = get_salaries_table()
        for idx, salary in enumerate(salaries):
            table.add_row(*salary.to_rich_table_row(idx + 1))

        console.print(table)

    except ConnectError:
        console.print("❌ [red]Connection error[/red]. Please try again later.")


@app.command(name="ar", help="Generate salary by amount range.")
def generate_by_amount_range(  # noqa: PLR0913
    compensations_rate: Annotated[
        float,
        typer.Option(
            "--rate",
            "-r",
            help="Compensations rate",
            prompt=True,
            envvar="DEFAULT_GENERATE_COMPENSATIONS_RATE",
        ),
    ],
    start: Annotated[
        int,
        typer.Option(
            "--start",
            help="Start salary",
            prompt=True,
            envvar="DEFAULT_GENERATE_AMOUNT",
        ),
    ],
    stop: Annotated[
        int | None,
        typer.Option(
            "--stop",
            help="End salary",
        ),
    ] = None,
    step: Annotated[
        int | None,
        typer.Option(
            "--step",
            help="Step",
        ),
    ] = None,
    tax_id: TaxIdTyperParam = None,
    export: Annotated[
        ExportType | None,
        typer.Option(
            "--export",
            "-e",
            help="Export type",
        ),
    ] = None,
):
    if stop and start > stop:
        message = "❌ Start must be less than stop"
        raise ValueError(message)

    if step and stop and step > stop:
        message = "❌ Step must be less than stop"
        raise ValueError(message)

    if step and stop and (stop - start) < step:
        message = "❌ Stop - Start must be greater than step"
        raise ValueError(message)

    if stop is None:
        stop = start * 10

    if step is None:
        step = start

    try:
        salaries = generate_salaries_by_amount_range(
            compensations_rate=compensations_rate,
            start=start,
            stop=stop,
            step=step,
            tax_id=tax_id,
        )

        if export is not None:
            filename = f"amount-range-{start}-{stop}-{step}"
            save_path = Path().home().resolve() / "Desktop"
            path = get_exporters()[export](filename, salaries, save_path)
            console.print(
                f"💾 file saved successfully to [green]{path}[/green]"
            )
            return

        table = get_salaries_table()
        for idx, salary in enumerate(salaries):
            table.add_row(*salary.to_rich_table_row(idx + 1))

        console.print(table)

    except ConnectError:
        console.print("❌ [red]Connection error[/red]. Please try again later.")
