import xlwings as xw
from syriantaxes import Rounder, SocialSecurity

from .models import SalaryInSchema, SettingsSchema


def calculate(
    rows: list[SalaryInSchema],
    settings: SettingsSchema,
    ss_obj: SocialSecurity,
    tax_rounder: Rounder,
    calculation_rounder: Rounder,
) -> None:
    for salary in rows:
        print(salary)
