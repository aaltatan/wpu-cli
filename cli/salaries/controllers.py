# ruff: noqa: B008
from collections.abc import Callable

import typer
import xlwings as xw
from syriantaxes import Rounder, SocialSecurity
from typer_di import Depends, TyperDI

from .dependencies import (
    get_calculation_rounder,
    get_ss_obj,
    get_taxes_rounder,
    get_writer_fn,
    read_rows,
    read_settings,
)
from .models import SalaryInSchema, SettingsSchema
from .options import WriteConfirmationOpt
from .services import SalaryCalculator

app = TyperDI()


@app.command(name="calc", no_args_is_help=True)
def calculate_cmd(  # noqa: PLR0913
    rows: list[SalaryInSchema] = Depends(read_rows),
    settings: SettingsSchema = Depends(read_settings),
    ss_obj: SocialSecurity = Depends(get_ss_obj),
    tax_rounder: Rounder = Depends(get_taxes_rounder),
    calculation_rounder: Rounder = Depends(get_calculation_rounder),
    write: WriteConfirmationOpt = False,  # noqa: FBT002
    writer_fn: Callable[[list[list[float]]], xw.Sheet] = Depends(get_writer_fn),
) -> None:
    data = [
        SalaryCalculator(row, settings, calculation_rounder, tax_rounder, ss_obj)
        .calculate()
        .as_row()
        for row in rows
    ]

    if write:
        ws = writer_fn(data)
        typer.echo(f"Results written to {ws.name}")

    total = sum(row[-1] for row in data)
    typer.echo(f"{total = :,.2f}")
