# ruff: noqa: B008
from devtools import debug
from syriantaxes import Rounder, SocialSecurity
from typer_di import Depends, TyperDI

from .dependencies import (
    get_calculation_rounder,
    get_ss_obj,
    get_taxes_rounder,
    load_rows,
    load_settings,
)
from .models import SalaryInSchema, SettingsSchema

app = TyperDI()


@app.command(name="calc")
def calculate_cmd(
    rows: list[SalaryInSchema] = Depends(load_rows),
    settings: SettingsSchema = Depends(load_settings),
    ss_obj: SocialSecurity = Depends(get_ss_obj),
    tax_rounder: Rounder = Depends(get_taxes_rounder),
    calculation_rounder: Rounder = Depends(get_calculation_rounder),
) -> None:
    for salary in rows:
        debug(salary)
        print("#" * 100)
