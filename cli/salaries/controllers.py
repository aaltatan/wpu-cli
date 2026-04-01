# ruff: noqa: B008
import typer
import xlwings as xw
from syriantaxes import Rounder, SocialSecurity
from typer_di import Depends, TyperDI

from .dependencies import (
    get_calculation_rounder,
    get_data_worksheet,
    get_ss_obj,
    get_taxes_rounder,
    read_rows,
    read_settings,
)
from .mappers import CALCULATED_END_COLUMN, CALCULATED_START_COLUMN, START_ROW
from .models import SalaryInSchema, SettingsSchema
from .services import SalaryCalculator

app = TyperDI()


@app.command(name="calc", no_args_is_help=True)
def calculate_cmd(  # noqa: PLR0913
    rows: list[SalaryInSchema] = Depends(read_rows),
    settings: SettingsSchema = Depends(read_settings),
    ss_obj: SocialSecurity = Depends(get_ss_obj),
    tax_rounder: Rounder = Depends(get_taxes_rounder),
    calculation_rounder: Rounder = Depends(get_calculation_rounder),
    ws: xw.Sheet = Depends(get_data_worksheet),
) -> None:
    data = [
        SalaryCalculator(row, settings, calculation_rounder, tax_rounder, ss_obj)
        .calculate()
        .as_row()
        for row in rows
    ]

    ws.range(f"{CALCULATED_START_COLUMN}{START_ROW}:{CALCULATED_END_COLUMN}{len(data)}").options(
        index=False
    ).value = data

    typer.echo(f"Results written to {ws.name}")
